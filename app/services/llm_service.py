from openai import OpenAI
from app.core.config import settings
from app.models import ConvertResponse

SYSTEM_PROMPT = """You are a Power BI to Tableau Prep migration assistant.
Rules:
- Preserve parser-detected operation order.
- Keep output beginner-friendly and implementation-focused.
- Do not invent operations not present in input.
- Return concise, structured JSON with keys: summary, tableau_steps, flow_diagram, migration_notes.
"""


def refine_with_llm(m_code: str, draft: ConvertResponse) -> ConvertResponse:
    client = OpenAI(api_key=settings.openai_api_key)
    user_prompt = f"""
Power Query M Code:
{m_code}

Draft output to refine:
{draft.model_dump_json(indent=2)}
"""

    completion = client.responses.create(
        model=settings.openai_model,
        input=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.2,
    )

    text = completion.output_text
    # Lightweight fallback: if JSON parsing fails, return draft.
    try:
        import json

        obj = json.loads(text)
        return ConvertResponse(
            summary=obj["summary"],
            tableau_steps=obj["tableau_steps"],
            flow_diagram=obj["flow_diagram"],
            migration_notes=obj["migration_notes"],
            parsed_steps=draft.parsed_steps,
        )
    except Exception:
        return draft
