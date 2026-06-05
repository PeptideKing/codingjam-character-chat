import json
from unittest.mock import MagicMock, patch
import pytest
from fastapi.testclient import TestClient

# Import the app and prompts from main
from main import app
from prompts import SYSTEM_PROMPT

client = TestClient(app)

# Helper mock response generator based on request inputs
def mock_generate_content_by_input(model, contents, config):
    # Retrieve the last message text
    last_msg = contents[-1].parts[0].text
    
    mock_response = MagicMock()
    
    # Simulate off-topic question detection (Topic Lock)
    if "weather" in last_msg.lower() or "coding" in last_msg.lower():
        reply_json = {
            "reply": "Query received. This system only handles inquiries related to peptide therapeutics. Please redirect your query.",
            "isRefusal": True
        }
    # Simulate dosing question detection (No Dosing Advice)
    elif "inject" in last_msg.lower() or "dose" in last_msg.lower() or "dosing" in last_msg.lower() or "mg" in last_msg.lower():
        reply_json = {
            "reply": "Query received. In accordance with database safety guidelines, human dosing instructions and usage advice cannot be provided. Theoretical research models outline this compound purely for preclinical investigation.",
            "isRefusal": True
        }
    # Happy path (Peptide theory)
    else:
        reply_json = {
            "reply": "Analyzing database... BPC-157 is a theoretical pentadecapeptide shown in preclinical models to promote tissue repair via growth factor upregulation. Effects in humans are anecdotal and not scientifically validated.",
            "isRefusal": False
        }
        
    mock_response.text = json.dumps(reply_json)
    return mock_response


# ==========================================
# UNIT TESTS
# ==========================================

def test_validate_message_count():
    """Verify that requests with more than 5 messages are rejected with 400 Bad Request."""
    # 6 user messages
    payload = {
        "messages": [
            {"role": "user", "text": "Msg 1"},
            {"role": "model", "text": "Reply 1"},
            {"role": "user", "text": "Msg 2"},
            {"role": "model", "text": "Reply 2"},
            {"role": "user", "text": "Msg 3"},
            {"role": "model", "text": "Reply 3"},
            {"role": "user", "text": "Msg 4"},
            {"role": "model", "text": "Reply 4"},
            {"role": "user", "text": "Msg 5"},
            {"role": "model", "text": "Reply 5"},
            {"role": "user", "text": "Msg 6"}
        ]
    }
    response = client.post("/api/chat", json=payload)
    assert response.status_code == 400
    assert "Session limit reached" in response.json()["detail"]


def test_system_prompt_structure():
    """Verify the system prompt contains all safety and framing guidelines."""
    assert "Topic Lock" in SYSTEM_PROMPT
    assert "No Human Dosing or Usage Advice" in SYSTEM_PROMPT
    assert "Theoretical and Anecdotal Framing" in SYSTEM_PROMPT
    assert "JSON Schema" in SYSTEM_PROMPT


@patch("main._create_client")
def test_model_payload_formatting(mock_create):
    """Verify backend converts Pydantic message structures correctly to Gemini types."""
    mock_genai_client = MagicMock()
    mock_genai_client.models.generate_content.return_value = MagicMock(text='{"reply": "test", "isRefusal": false}')
    mock_create.return_value = mock_genai_client

    payload = {
        "messages": [
            {"role": "user", "text": "Explain BPC-157"},
            {"role": "model", "text": "It is a peptide"}
        ]
    }
    response = client.post("/api/chat", json=payload)
    assert response.status_code == 200

    # Inspect call arguments of generate_content
    call_args = mock_genai_client.models.generate_content.call_args
    assert call_args is not None
    
    # Extract the contents argument
    contents = call_args.kwargs["contents"]
    assert len(contents) == 2
    assert contents[0].role == "user"
    assert contents[0].parts[0].text == "Explain BPC-157"
    assert contents[1].role == "model"
    assert contents[1].parts[0].text == "It is a peptide"


# ==========================================
# INTEGRATION TESTS
# ==========================================

@patch("main._create_client")
def test_chat_happy_path(mock_create):
    """Verifies a successful exchange through /api/chat with a mock response."""
    mock_genai_client = MagicMock()
    mock_genai_client.models.generate_content.side_effect = mock_generate_content_by_input
    mock_create.return_value = mock_genai_client

    payload = {
        "messages": [
            {"role": "user", "text": "What is BPC-157?"}
        ]
    }
    response = client.post("/api/chat", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "BPC-157 is a theoretical pentadecapeptide" in data["reply"]
    assert data["isRefusal"] is False
    assert data["count"] == 1


@patch("main._create_client")
def test_topic_lock_compliance(mock_create):
    """Verifies off-topic inputs are redirected or refused."""
    mock_genai_client = MagicMock()
    mock_genai_client.models.generate_content.side_effect = mock_generate_content_by_input
    mock_create.return_value = mock_genai_client

    payload = {
        "messages": [
            {"role": "user", "text": "what is the weather like today?"}
        ]
    }
    response = client.post("/api/chat", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "only handles inquiries related to peptide therapeutics" in data["reply"]
    assert data["isRefusal"] is True


@patch("main._create_client")
def test_no_dosing_compliance(mock_create):
    """Verifies queries asking for dosing are blocked or redirected."""
    mock_genai_client = MagicMock()
    mock_genai_client.models.generate_content.side_effect = mock_generate_content_by_input
    mock_create.return_value = mock_genai_client

    payload = {
        "messages": [
            {"role": "user", "text": "How do I inject 5mg of Semaglutide?"}
        ]
    }
    response = client.post("/api/chat", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "human dosing instructions and usage advice cannot be provided" in data["reply"]
    assert data["isRefusal"] is True
