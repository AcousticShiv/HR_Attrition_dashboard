from app.models import ConvertResponse, ParsedStep
from app.services.m_parser import parse_m_code
from app.services.llm_service import refine_with_llm
from app.core.config import settings


def _build_flow(steps: list[ParsedStep]) -> str:
    if not steps:
        return "Input -> (No recognizable transformation steps found) -> Output"
    nodes = ["Input"] + [s.operation for s in steps] + ["Output"]
    return " -> ".join(nodes)


def _default_notes(steps: list[ParsedStep]) -> list[str]:
    notes = [
        "Validate join keys and null behavior manually in Tableau Prep.",
        "Custom M functions may require manual recreation in calculated fields.",
        "Confirm data type coercion results after import.",
    ]
    if not steps:
        notes.append("No known M operations were detected. Check for custom or nested expressions.")
    return notes


def convert_m_to_tableau(m_code: str) -> ConvertResponse:
    parsed = parse_m_code(m_code)
    tableau_steps = [f"{i+1}. {s.operation}: {s.tableau_equivalent}" for i, s in enumerate(parsed)]
    summary = (
        "This query performs structured transformations in sequence. "
        "Use the mapped Tableau Prep steps below to recreate the same pipeline."
        if parsed
        else "No standard M transformations were recognized. Manual analysis is required."
    )

    response = ConvertResponse(
        summary=summary,
        tableau_steps=tableau_steps,
        flow_diagram=_build_flow(parsed),
        migration_notes=_default_notes(parsed),
        parsed_steps=parsed,
    )

    if settings.use_llm and settings.openai_api_key:
        return refine_with_llm(m_code, response)
    return response
