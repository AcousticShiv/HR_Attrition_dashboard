import re
from app.models import ParsedStep

OPERATION_PATTERNS = [
    (r"Table\.RenameColumns", "Rename columns", "Clean Step > Rename Field"),
    (r"Table\.TransformColumnTypes", "Change data types", "Clean Step > Change Data Type"),
    (r"Table\.RemoveColumns", "Remove columns", "Clean Step > Remove Fields"),
    (r"Table\.NestedJoin|Table\.Join", "Merge queries", "Join Step"),
    (r"Table\.Combine", "Append queries", "Union Step"),
    (r"Table\.AddColumn", "Calculated/conditional column", "Calculated Field in Clean Step"),
    (r"Table\.Group", "Group by", "Aggregate Step"),
    (r"Table\.Pivot", "Pivot", "Pivot Step"),
    (r"Table\.Unpivot|Table\.UnpivotOtherColumns", "Unpivot", "Pivot Step (Unpivot)"),
    (r"Table\.SelectRows", "Filter rows", "Clean Step > Filter"),
    (r"Table\.Sort", "Sort rows", "Clean Step > Sort"),
]


def parse_m_code(m_code: str) -> list[ParsedStep]:
    steps: list[ParsedStep] = []
    for pattern, operation, tableau_equivalent in OPERATION_PATTERNS:
        for match in re.finditer(pattern, m_code):
            steps.append(
                ParsedStep(
                    operation=operation,
                    source_pattern=match.group(0),
                    tableau_equivalent=tableau_equivalent,
                    explanation=(
                        f"Detected '{operation}' via '{match.group(0)}'. "
                        f"Map this to Tableau Prep: {tableau_equivalent}."
                    ),
                )
            )

    # preserve first-seen order by source index
    steps = sorted(steps, key=lambda s: m_code.find(s.source_pattern))
    return steps
