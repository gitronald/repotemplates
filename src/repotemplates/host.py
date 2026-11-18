"""The pkgskills host: the skills repotemplates ships, and how they are invoked.

``repotemplates skill <name>`` prints a body from the installed release, and
``repotemplates install`` writes a version-stamped stub where Claude Code and
Codex read skills. Every skill acts on other repos (upgrading one, enrolling one
in Renovate, checking whether one publishes), so the default install is global;
``--local`` stays available.
``test-init`` is not here: it tests a repotemplates checkout, so it stays in the
checkout's ``.claude/skills/``.
"""

from __future__ import annotations

from pkgskills import Host, Skill

__all__ = ["HOST"]

HOST = Host(
    dist="repotemplates",
    cli="repotemplates",
    prompts="repotemplates.prompts",
    artifacts=(
        Skill(name="install-template", sources=("install-template/SKILL.md",)),
        Skill(name="install-renovatabot", sources=("install-renovatabot/SKILL.md",)),
        Skill(name="check-publishing", sources=("check-publishing/SKILL.md",)),
    ),
    render_cli=True,
    modes=("global", "local"),
)
