# Release Checklist — RC → GA
- [ ] CI green on main (black/ruff/mypy/unit/acceptance/coverage/build/audit)
- [ ] Acceptance tests pass for AC-GRAMMAR-01 and perf budgets
- [ ] Version bump (semver) + git tag
- [ ] CHANGELOG updated with user-facing notes
- [ ] Docs updated (README/API)
- [ ] Release notes drafted (SPRINT_LOG.md summary)
- [ ] Smoke test on clean venv/clone
- [ ] Artifacts attached (sdist/wheel)
Go/No-Go:
- [ ] Go → publish / announce
- [ ] No-Go → log reasons in SPRINT_LOG.md and create follow-up tasks

