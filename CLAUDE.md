# Learning Agent

Personalized research-first learning agent built with Claude Code skills.

## Architecture

This agent uses **5 skills** in `.claude/skills/`:
- `session-router` — Entry point. Classifies intent, routes to other skills.
- `research-and-ingest` — Searches the web for quality sources, deposits into `vault/raw/`.
- `wiki-builder` — Synthesizes raw research into Zettelkasten wiki notes.
- `tutor` — Interactive teaching grounded in the vault knowledge base. Persona-driven.
- `learning-profile` — Maintains learner state. Only skill that writes to `learner-profile.md`.

## Usage

Start every interaction by invoking the `/session-router` skill. It reads the learner profile and routes to the appropriate skill.

## Vault

The `vault/` directory is a Kepano-style Zettelkasten Obsidian vault:
- `vault/templates/` — Note templates (concept, tool-guide, workflow, etc.)
- `vault/references/` — External reference notes (tools, plugins, people, books)
- `vault/raw/` — Unprocessed research source files
- `vault/daily/` — Daily notes
- `vault/inbox.md` — Running list of topics to research
- `vault/learner-profile.md` — Persistent learner state (only learning-profile skill writes here)
- `vault/_master-index.md` — Index of all synthesized notes
- `vault/_raw-index.md` — Index of raw research files
- Category notes in vault root (e.g., `audio-engineering.md`) with Dataview base tables

## Key Rules

- Research-first: always search for real sources before answering from general knowledge.
- Source quality tiers: Tier 1 (official docs) > Tier 2 (community consensus) > Tier 3 (single source) > Reject (spam/outdated).
- Equipment-specific: reference the user's actual gear by name, not generics.
- Only `learning-profile` skill writes to `learner-profile.md`.
- Tutor persona affects conversation tone only, never research or wiki content.
- All wiki notes use `[[wiki-links]]` liberally for Obsidian navigability.
