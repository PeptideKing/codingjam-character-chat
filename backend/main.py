"""AmazonPeptide Assistant — FastAPI backend server."""

import json
import os
from typing import List

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from google import genai
from google.genai import types
from pydantic import BaseModel, Field

from prompts import SYSTEM_PROMPT

load_dotenv()

app = FastAPI(title="AmazonPeptide Assistant")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Use gemini-2.5-flash as specified in engineering.md
MODEL = "gemini-2.5-flash"

def _create_client():
    """Create a fresh Gemini client for each request."""
    api_key = os.getenv("GEMINI_API_KEY")
    if api_key:
        return genai.Client(api_key=api_key)
    # Fallback to Vertex AI if key not provided
    return genai.Client(
        vertexai=True,
        project=os.getenv("GOOGLE_CLOUD_PROJECT"),
        location=os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1"),
    )


# --- Models ---

class Message(BaseModel):
    role: str = Field(description="The role of the sender: 'user' or 'model'")
    text: str = Field(description="The message text content")


class ChatRequest(BaseModel):
    messages: List[Message] = Field(description="Chronological message history for the session")


# --- Routes ---

@app.post("/api/chat")
async def chat(request: ChatRequest):
    """Processes a user message, enforces topic locks & safety checks, and queries Gemini."""
    
    if not request.messages:
        raise HTTPException(
            status_code=400,
            detail="Message history cannot be empty.",
        )

    # Count user messages in the session
    user_message_count = sum(1 for m in request.messages if m.role == "user")
    if user_message_count > 5:
        raise HTTPException(
            status_code=400,
            detail="Session limit reached. Maximum 5 messages allowed.",
        )

    # Transform messages list into the format required by the google-genai SDK
    gemini_contents = []
    for msg in request.messages:
        role = "model" if msg.role in ("model", "assistant") else "user"
        gemini_contents.append(
            types.Content(
                role=role,
                parts=[types.Part.from_text(text=msg.text)]
            )
        )

    try:
        client = _create_client()
        response = client.models.generate_content(
            model=MODEL,
            contents=gemini_contents,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                temperature=0.2,  # Low temperature for strict rule-following
                response_mime_type="application/json",
            ),
        )

        response_text = response.text.strip()

        # Strip markdown code fences if outputted by the model
        if response_text.startswith("```"):
            # split first line
            response_text = response_text.split("\n", 1)[1]
            if response_text.endswith("```"):
                response_text = response_text[:-3]
            response_text = response_text.strip()

        data = json.loads(response_text)

        # Validate fields returned by Gemini JSON schema
        if "reply" not in data or "isRefusal" not in data:
            raise ValueError("Invalid response schema from Gemini model")

        return {
            "reply": data["reply"],
            "isRefusal": data["isRefusal"],
            "count": user_message_count
        }

    except json.JSONDecodeError as e:
        print(f"JSON parse error: {e}")
        raise HTTPException(
            status_code=500,
            detail="Query failed: Unable to parse database response.",
        )
    except ValueError as e:
        print(f"Validation error: {e}")
        raise HTTPException(
            status_code=500,
            detail="Query failed: Invalid database schema returned.",
        )
    except Exception as e:
        print(f"Generation error: {e}")
        raise HTTPException(
            status_code=500,
            detail="Query failed: Database connection timeout.",
        )


@app.get("/api/health")
async def health():
    """Health check endpoint."""
    return {"status": "ok"}


# Mount frontend static files
frontend_path = os.path.join(os.path.dirname(__file__), "..", "frontend")
if os.path.exists(frontend_path):
    app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")
