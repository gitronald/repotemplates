---
id: 16
slug: simplify-cli-and-docs
status: draft
branch:
created: 2026-11-14T10:26:33-08:00
concluded:
pr:
---

# Simplify the CLI helpers and state current rules in the docs

## Plan

A cleanup pass over the CLI, the scaffold script, the test helpers, and the
docs, proposed by a remote session and reauthored here. No behavior or output
changes; the docs fix guidance that had gone stale.

### Frozen view

- Reauthored from `origin/ccr-decbf8f4-724h2i` @ `50c198e5`
- 4 commits, 23 files (+404/-367), forked at `dev` @ `5f1d6d8c` (the current tip)
- No PR on the remote branch
- Gate: `uv run ruff check . && uv run ruff format --check .`, `uv run pyrefly
  check`, `uv run pytest`, `/bin/bash tests/portability.test.sh`, and
  `shellcheck` on every tracked `*.sh`. `tests/init.test.sh` runs once per
  committed batch that touches `scripts/`, since it refuses uncommitted changes

Per-commit review: [review.md](review.md).

### Batches

Each batch is one commit, retyped by hand from the remote diff.

| # | Desktop subject | Remote sha | Fixes |
|---|---|---|---|
| 1 | `simplify stamp and prerelease steps, probe git once` | 115b735e | restore the `stamp` command's docstring indentation, which the remote diff broke (it is the command's `--help` text) |
| 2 | `simplify init.sh option parsing and trim comments` | 3c61218e | none |
| 3 | `share the cli runner and make_repo type in conftest` | 3856acf7 | none |
| 4 | `update docs to current rules and fix stale guidance` | 50c198e5 | the changelog's git-call count is stated only if measured here; the README step list is not claimed to follow `init.sh`'s exact order (the `--deps` pruning runs between the copy and the placeholder pass) |

Order: code first, then tests that import from it, then the docs that describe
it. No hand-owned data and no template-owned file (`template/`) is touched, so
the release manifest is unaffected.

### Drops

None.

### Open questions

1. Batches 1, 2, and 4 drop release numbers from comments and from the
   `install-template` skill ("templates 0.5.0 through 0.8.4 shipped one", "from
   before 0.8.2", "before 0.10.0"), keeping each rule and leaving the history
   to the changelog. Keep that removal, or keep the version numbers?
