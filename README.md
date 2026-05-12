# Power Query M → Tableau Prep Migration Assistant

A production-oriented starter app that converts Power Query **M code** into beginner-friendly Tableau Prep migration guidance.

## What this app returns
1. Plain-English transformation explanation
2. Tableau Prep step-by-step instructions
3. Text flow representation
4. Migration notes / limitations

## Tech stack
- **Backend**: FastAPI (Python)
- **Frontend**: Streamlit
- **LLM**: OpenAI API (optional enhancement layer)
- **Validation**: Pydantic

## Quick start

### 1) Create environment
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2) Configure env
```bash
cp .env.example .env
```
Set `OPENAI_API_KEY` if you want LLM-enhanced output.

### 3) Run backend
```bash
uvicorn app.main:app --reload --port 8000
```

### 4) Run frontend
```bash
streamlit run frontend/streamlit_app.py
```

## API endpoint
- `POST /api/v1/convert`

## Notes
- The app includes a deterministic parser/mapping layer first.
- If LLM is enabled, it refines wording while preserving transformation order and parser-detected steps.
