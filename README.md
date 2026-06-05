# AmazonPeptide Assistant

An AI-powered, theoretical research chatbot widget integrated into a retro early-2000s mockup of the **AmazonPeptide** website. It provides authoritative, encyclopedic knowledge about peptide therapeutics while strictly adhering to safety guardrails.

---

## What This App Does

The application consists of two parts:
1. **Mockup E-Commerce Frontend**: A pixel-perfect recreation of the classic AmazonPeptide web layout, including search sidebars, product panels (e.g., Semaglutide, BPC-157), and styling.
2. **Embeddable Chat Widget**: A floating help tab in the bottom-right corner that expands into an interactive assistant. 
   - **Encyclopedic Coverage**: Answers theoretical research questions about biochemistry, cellular receptors, and mechanism pathways of peptides.
   - **Safety / Compliance Guardrails**: Strictly refuses to provide human dosing instructions, injection guidelines, or administration frequencies, framing all human effects as purely anecdotal and theoretical.
   - **Message Cap**: Limits chats to a maximum of 5 messages per session to encourage concise, safety-aligned research inquiries.

---

## Project Structure

```text
coding-jam-setup/
├── backend/
│   ├── main.py            # FastAPI server & Gemini API routing
│   ├── prompts.py         # Safety system prompts for the model
│   ├── pyproject.toml     # Python package and dependency definitions
│   └── .env               # Local environment secrets (ignored by Git)
├── frontend/
│   ├── index.html         # Main mockup website containing the widget markup
│   ├── style.css          # Main website styles
│   ├── widget.js          # Chat widget interactive state & typewriter effect
│   └── widget.css         # Chat widget retro visual styling
├── product.md             # Product requirements and scope cuts (Source of Truth)
├── ui.md                  # UX design states, visual language, and flows (Source of Truth)
├── engineering.md         # Architecture, APIs, schemas, and test plans (Source of Truth)
└── README.md              # This guide
```

---

## Installation & Setup

Ensure you have [uv](https://github.com/astral-sh/uv) installed on your system.

1. **Clone the repository** (if not already done).
2. **Navigate to the backend folder**:
   ```bash
   cd backend
   ```
3. **Install dependencies** (creates a local virtual environment and locks dependencies):
   ```bash
   uv sync
   ```
4. **Configure your API Key**:
   Create a `.env` file inside the `backend/` directory:
   ```text
   GEMINI_API_KEY=your_gemini_api_key_here
   ```
   *(Note: `.env` is listed in `.gitignore` to prevent secret leaks).*

---

## Running the App

### 1. Start the Development Server
From the `backend/` directory, run:
```bash
uv run uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

### 2. View in Browser
Open your browser and navigate to:
👉 **[http://127.0.0.1:8000](http://127.0.0.1:8000)**

---

## Running Automated Tests

The backend includes a comprehensive unit and integration test suite using `pytest` and `httpx`. The tests mock all Gemini API connections for deterministic and cost-free execution.

From the `backend/` directory, run:
```bash
PYTHONPATH=. uv run pytest -v
```

---

## Specifications & Design Sources of Truth

For any deep technical design, visual flow, or feature scope questions, refer to the three documents in the project root:
* **[product.md](product.md)**: Details the user needs, core functional constraints (such as the 5-message exchange limit), and what features are out-of-scope.
* **[ui.md](ui.md)**: Specs the collapsed/expanded UI widget specs, typewriter transitions, retro colors, and WCAG AA contrast standards.
* **[engineering.md](engineering.md)**: Covers backend architecture diagrams, JSON request/response structures, and mock testing suites.
