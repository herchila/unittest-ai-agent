# Contributing

## Ground rules
- Be respectful. Follow our Code of Conduct.
- Small, focused PRs are easiest to review.

## Workflow
1. Open an issue (or comment on an existing one) to align on scope.
2. Fork & create a branch: feat/<short-name> or fix/<short-name>.
3. Follow Conventional Commits for messages.
4. Add/adjust tests and docs.
5. Open a PR referencing the issue. Keep it under ~300 lines if possible.

## Development setup
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
pre-commit install
pytest
```

## Quality bar

* Lint/format: ruff + black must pass.
* Tests: pytest must be green. Aim for coverage ≥80% over time.
* CI must pass for merging.

## Reviews & Merging

* At least one approval is required.
* Squash & merge with a clean title (Conventional Commit).
