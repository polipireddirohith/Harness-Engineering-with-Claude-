# Test Manifest — System 2

- Rubric baseline: **17 core tests**
- Current pytest result: **30 passed**
- Alignment: 17 core requirement checks + 13 supplementary verification checks.

## Core requirement checks (17)
- `test_transcript.py`: 5
- `test_pruner.py`: 4
- `test_assemble.py`: 3
- `test_compressor.py`: 4
- `test_case_facts.py::test_required_fields_has_12_entries`: 1

## Supplementary checks (13)
- `test_antipatterns.py`: 5
- Remaining `test_case_facts.py`: 4
- `test_tokens.py`: 4

The supplementary checks were added to protect deterministic invariants, token-count methodology, schema/error handling, and anti-patterns. They are intentionally retained.
