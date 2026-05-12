from app.services.m_parser import parse_m_code


def test_detects_common_operations_in_order():
    m = """
let
  Source = Csv.Document("x"),
  Renamed = Table.RenameColumns(Source, {{"a", "b"}}),
  Typed = Table.TransformColumnTypes(Renamed, {{"b", type text}}),
  Filtered = Table.SelectRows(Typed, each [b] <> null)
in
  Filtered
"""
    steps = parse_m_code(m)
    assert [s.operation for s in steps] == ["Rename columns", "Change data types", "Filter rows"]
