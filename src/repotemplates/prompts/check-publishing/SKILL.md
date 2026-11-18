---
name: check-publishing
description: Establish whether a repo scaffolded from or synced with repotemplates actually publishes to PyPI. Use before saying that such a repo is or is not published, released, or "on PyPI", for one repo or an inventory of many, and whenever a `publish.yml`, a `pypi` environment, or a Trusted Publisher step is about to be read as evidence that a package ships.
---

# Check publishing

Every repo scaffolded from repotemplates starts with the template's
`.github/workflows/publish.yml`, and an upgrade syncs it into every package repo
(an app or site leaves it out and lists it in the stamp's `omit`). The workflow
is a no-op until the `PUBLISH_ENABLED` variable is `true`: a tag push matching
`v*` still starts a run, and both of its jobs skip.

So never infer "published to PyPI" from the workflow file, a `pypi` environment,
or the `pypa/gh-action-pypi-publish` (Trusted Publisher) step. The template
writes all three whether or not anyone opted in, so they look the same in a repo
that has never published.

## What the template ships

Take the gate from the installed release, not from memory: `{cli} path template`
prints the template's directory, and its `.github/workflows/publish.yml` is the
reference. The opt-in steps are in the
[trusted-publishers guide](https://github.com/gitronald/repotemplates/blob/main/docs/guides/trusted-publishers.md),
which a scaffolded repo does not carry.

The consumer's own copy decides what that repo does, and it may have been
edited. `{cli} check <path>` reports its `publish.yml` row: `current` and
`matches` (an earlier release's copy) are the template's own text, and `missing`
and `omitted` mean the repo has no such workflow. For `one-off`, `kept`, or
`kept-behind`, the repo has changed the file, so read the copy before applying
the checks below: it may have dropped the gate or publish on another trigger.

## The three checks

1. **The variable.** `gh variable get PUBLISH_ENABLED -R OWNER/REPO` reads the
   repository level, and unset (the command exits non-zero) means off there.
   The gate reads the `vars` context, which also takes organization variables
   shared with the repo; a repository variable of the same name wins. For a repo
   an organization owns (`gh repo view OWNER/REPO --json isInOrganization`),
   also read `gh api repos/OWNER/REPO/actions/organization-variables`, which
   lists the organization variables shared with that repo and their values.
   `gh variable get --org` needs the `admin:org` token scope, so prefer that
   endpoint. The build job names no environment, so a variable set on the
   `pypi` environment cannot open the gate. Actions compares strings without
   regard to case, so `True` opens it as well as `true`.
2. **The run history.** `gh run list --workflow publish.yml -R OWNER/REPO` lists
   the tag runs. A run whose jobs skipped shipped nothing. A release shipped only
   where the `publish` job ran and succeeded (`gh run view <run-id> -R
   OWNER/REPO` lists the jobs). The variable says whether the next tag will
   publish; the history says whether any tag did.
3. **The registry.** `curl -s -o /dev/null -w '%{http_code}'
   https://pypi.org/pypi/<name>/json`, where `<name>` is `project.name` in the
   repo's `pyproject.toml`, which can differ from the repo name. `404` means no
   such project. A `200` is not proof on its own, since another author can hold
   the name: check that the project's author and source URLs
   (`curl -s https://pypi.org/pypi/<name>/json | jq '.info | {author,
   author_email, project_urls}'`) name the expected owner and repository.

## Reading them together

- Variable unset, no `publish` job ever ran, registry `404`: not published.
- Variable `true`, a `publish` job succeeded, registry `200` for the expected
  project: published through the template's workflow.
- Variable `true` with no successful `publish` job: opted in, nothing shipped
  yet. Either no tag has been pushed since, or the publish fails (the guide's
  Troubleshooting section covers the usual causes).
- Variable unset and a `200` for the expected project: the repo publishes, or
  once did, some other way. A past successful `publish` job means the gate was
  open then and has closed since. Otherwise read the repo's own `publish.yml`
  and its other workflows; a manual upload leaves no run at all.

Report each repo's three readings alongside the verdict, so a reader can see
which check settled it.
