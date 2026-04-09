# Learning Agent — Integrated Second Brain

Personalized research-first learning agent with self-evolving knowledge management. Built with Claude Code skills + [obsidian-second-brain](https://github.com/eugeniughelbur/obsidian-second-brain) integration.

## Architecture

### Layer 1: Intent Router
- **session-router** — Entry point. Classifies intent, routes to learning or vault management skills.

### Layer 2: Learning Pipeline (7 local skills)
- `onboarding` — First-time user setup and deep domain intake with knowledge distillation.
- `research-and-ingest` — Searches the web for quality sources, deposits into `vault/raw/`.
- `wiki-builder` — Synthesizes raw research into Zettelkasten wiki notes.
- `tutor` — Interactive teaching grounded in the vault knowledge base. Persona-driven.
- `learning-profile` — Maintains learner state. Only skill that writes to `learner-profile.md`.
- `reflection` — Nightly synthesis. Reads episodes, extracts patterns, creates daily notes.

### Layer 3: Vault Management (obsidian-second-brain — 24 global commands)
- `/obsidian-save` — Extract conversation insights → episodic notes in `vault/daily/`
- `/obsidian-synthesize` — Process raw sources → synthesized wiki notes
- `/obsidian-health` — Audit vault for gaps, contradictions, orphans
- `/obsidian-emerge` — Surface 30-day patterns → `[[evergreen]]` notes
- `/obsidian-connect [A] [B]` — Bridge domains, create cross-domain connections
- Plus 19 more: ingest, daily, find, recap, world, challenge, reconcile, log, task, person, decide, capture, review, board, project, adr, visualize, export, graduate

### Layer 4: Automation
- **PostCompact hook** — Background agent saves learnings + synthesizes + health checks after context compact
- **Scheduled agents** — Morning briefing (8 AM), nightly reflection (10 PM), weekly review (Fri 6 PM), health audit (Sun 9 AM)

## Three-Layer Memory Model

| Layer | What | Where | Created by |
|---|---|---|---|
| Working | Session context, current focus | In-memory (conversation) | Automatic |
| Episodic | Timestamped interaction records | `vault/daily/` | `/obsidian-save`, tutor wrap-up |
| Semantic | Distilled knowledge, patterns | `vault/` root (wiki notes, evergreens) | wiki-builder, `/obsidian-synthesize`, reflection |

**Feedback loop:** conversation → episode → pattern extraction → semantic update → informed future conversations

## Usage

**IMPORTANT: On EVERY user message, invoke the `/session-router` skill FIRST before doing anything else.** Do not answer directly — always route through session-router. This is the agent's entry point. It reads the learner profile, classifies intent, and dispatches to the correct skill. If the learner profile is blank, session-router auto-routes to onboarding.

The only exceptions: if the user is explicitly asking about the project itself (e.g., "what files are in this repo"), answer directly.

## Vault

The `vault/` directory is a Kepano-style Zettelkasten Obsidian vault:
- `vault/_CLAUDE.md` — Operating manual (teaches obsidian-* skills about our vault structure)
- `vault/templates/` — Note templates (concept, tool-guide, workflow, exercise, lesson, evergreen, research-source, category, weekly-review, reference, episode, daily-note)
- `vault/references/` — External reference notes (tools, plugins, people, books, hardware)
- `vault/raw/` — Unprocessed research source files
- `vault/daily/` — Episodes (session extracts) + daily reflection notes
- `vault/attachments/` — Images, PDFs, media
- `vault/inbox.md` — Running list of topics to research
- `vault/learner-profile.md` — Persistent learner state (only learning-profile skill writes here)
- `vault/log.md` — Activity timeline (auto-maintained by agents)
- `vault/_master-index.md` — Index of all synthesized notes
- `vault/_raw-index.md` — Index of raw research files
- Category notes in vault root (e.g., `audio-engineering.md`) with Dataview base tables

## Key Rules

- Research-first: always search for real sources before answering from general knowledge.
- Source quality tiers: Tier 1 (official docs) > Tier 2 (community consensus) > Tier 3 (single source) > Reject (spam/outdated).
- Equipment-specific: reference the user's actual gear by name, not generics.
- Only `learning-profile` skill writes to `learner-profile.md`.
- First-time users are routed to `onboarding` automatically by `session-router`.
- `onboarding` is the only skill besides `learning-profile` that writes to `learner-profile.md` (during initial setup only).
- Domain intake classifies knowledge as solid/partial/misconception — tutor adapts mode accordingly.
- Tutor persona affects conversation tone only, never research or wiki content.
- All wiki notes use `[[wiki-links]]` liberally for Obsidian navigability.
- Vault is Kepano-flat: no nested wiki/ subdirectories. See `vault/_CLAUDE.md` for full structure rules.
- Episodes capture every tutoring session → reflection extracts patterns nightly.
- Semantic memory is written by reflection/synthesis cycles, not during live sessions.
