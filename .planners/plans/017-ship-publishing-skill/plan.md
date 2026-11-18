---
id: 17
slug: ship-publishing-skill
status: draft
branch:
created: 2026-11-18T13:38:44-08:00
concluded:
pr:
---

# Ship the publishing check as a bundled skill

## Plan

Issue #75. Two notes about template behavior that is easy to misread from a
consumer repository live today in a hand-written user-level rule, outside the
package, and load into every session. Ship them from the package instead, where
they load on use and carry the release that knows the behavior.

### Decisions

1. **Publishing note: a new bundled skill, `check-publishing`.** It ships like the
   two existing skills: `src/repotemplates/prompts/check-publishing/SKILL.md`,
   registered in `src/repotemplates/host.py`, installed as a pkgskills stub, and
   printed by `repotemplates skill check-publishing`. A skill rather than a
   path-scoped rule, because the case that matters, an inventory across many
   repos, reads no file a `paths:` pattern could match. The description loads it
   when a session is about to say whether a repo scaffolded from the template
   publishes to PyPI, or reads meaning into `publish.yml`, a `pypi` environment,
   or a Trusted Publisher step. The body covers: publishing is off until
   `PUBLISH_ENABLED` is `true`; never infer "published" from the workflow's
   presence; the three checks (the variable, at repo level and through the
   org-variables endpoint for an org-owned repo; the publish workflow's run
   history; the registry, by `project.name`, with the author or source checked);
   what a `200` with the variable unset means; and that the template's own docs
   are the reference, not the consumer's copy. Each claim is re-derived from the
   template's `publish.yml` and `docs/guides/trusted-publishers.md`, not copied
   from the rule.
2. **Tracked-hooks note: the `install-template` skill**, at the upgrade step that
   runs `uv run pre-commit install --hook-type pre-commit --hook-type post-merge`.
   When `git config --get core.hooksPath` is set, pre-commit refuses and exits 1;
   the step counts as passing, and the setting is never unset.
3. **Dropped:** the history of the rename from `proj-template` (the
   `install-template` skill already handles the old stamp table) and the list of
   releases that seeded a permission list.

### Files

- `src/repotemplates/prompts/check-publishing/SKILL.md` (new)
- `src/repotemplates/host.py`: register the skill
- `src/repotemplates/prompts/install-template/SKILL.md`: the `core.hooksPath` case
- `tests/test_host.py`: add the skill to the parametrized list
- `.github/workflows/test.yml`: the wheel check lists the new body
- `README.md`, `.claude/CLAUDE.md`: name three skills
- `CHANGELOG.md`: `[Unreleased]` entries under Added and Changed

### Tests

`uv run pytest` covers spec conformance (name grammar, description length), the
commands a body names, the printed body, and the stubs a sandboxed install
writes. Then `uv run ruff check .`, `uv run ruff format --check .`, and
`uv run pyrefly check`.
