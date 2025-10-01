# Test Plan: W123 (Python)
## Commands
black --check .
ruff check .
mypy .
pytest -q
pytest -q tests/acceptance
pytest --cov=src --cov-report=term-missing --cov-fail-under=85
python -m build
pip-audit
# optional: bandit -r src -ll

## Acceptance Tests
- tests/acceptance/test_grammar_x.py::test_tokens_ABC
- tests/perf/test_parse_bench.py::test_parse_1k_lines_p95_lt_150ms

