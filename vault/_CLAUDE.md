---
created: 2026-04-09
categories: [[index]]
type: operating-manual
---

# Vault Operating Manual

This document teaches all Claude Code skills (including obsidian-* commands) how this vault is structured. Read this FIRST before any vault operation.

## Vault Identity

- **Name:** MyAgent Learning Vault
- **Style:** Kepano-style Zettelkasten (flat root, categories as properties)
- **Purpose:** Personalized research-first learning agent for multidisciplinary study

## Structure

```
vault/
├── templates/          — Note templates
├── references/         — External references (tools, plugins, people, books, hardware)
├── raw/                — Unprocessed research source files (one per source)
├── daily/              — Daily notes + episodic session records
├── attachments/        — Images, PDFs, media
├── _CLAUDE.md          — This file (operating manual)
├── _master-index.md    — Synthesized notes index (auto-maintained)
├── _raw-index.md       — Raw sources index (auto-maintained)
├── log.md              — Activity timeline
├── inbox.md            — Research queue (user + agent append)
├── learner-profile.md  — Persistent learner state (only learning-profile skill writes)
├── [category].md       — Category root notes with Dataview tables
└── [note].md           — Synthesized wiki notes (FLAT in root)
```

## CRITICAL: Deposit Rules

| Note type | Save to | Example |
|---|---|---|
| Raw research source | `vault/raw/[topic]-[source-type]-[date].md` | `raw/gain-staging-tutorial-2026-04-09.md` |
| Synthesized wiki note | `vault/[note-name].md` (flat root) | `gain-staging.md` |
| Episode (session extract) | `vault/daily/[YYYY-MM-DD]-[topic].md` | `daily/2026-04-09-gain-staging-session.md` |
| Daily summary | `vault/daily/[YYYY-MM-DD].md` | `daily/2026-04-09.md` |
| Reference note | `vault/references/[name].md` | `references/volt-476.md` |
| Category note | `vault/[category-name].md` | `audio-engineering.md` |
| Evergreen insight | `vault/[descriptive-name].md` (flat root) | `normalization-scales-inputs.md` |
| **NEVER** create | `vault/wiki/`, `vault/entities/`, `vault/concepts/` | These nested dirs DO NOT EXIST here |

## Frontmatter Schema

All notes use YAML frontmatter:

```yaml
---
created: YYYY-MM-DD
categories: [[category-name]]    # LINKS, not strings. Can have multiple.
tags: []
type: concept | tool-guide | workflow | exercise | lesson | evergreen | research-source | category | reference | episode | daily-note
difficulty: beginner | intermediate | advanced  # optional
rating: 1-7                      # Kepano-style (how essential)
sources: [[[raw/source-file]]]   # for synthesized notes
prerequisites: [[[wiki-links]]]  # required prereq notes
processed: false                 # for raw/ sources only
---
```

## Categories Are Properties, Not Folders

- Use links: `categories: [[audio-engineering]]` not `categories: audio-engineering`
- Category notes live in vault root with Dataview base tables
- A note can belong to multiple categories
- Create category notes from `vault/templates/category.md`

## Linking Convention

- Link the FIRST mention of any concept, tool, technique, or person
- Link even if target doesn't exist yet (creates research target = dangling link)
- Cross-domain links are a priority (audio ↔ photography ↔ knowledge-management)

## Episode Format (for /obsidian-save)

When extracting from a conversation, create an episode file:

```yaml
---
created: YYYY-MM-DD
categories: [[episode]]
episode_type: tutor-session | research-plan | synthesis-review | reflection
topic: [topic name]
domain: [[domain]]
learner_confidence: beginner | partial | solid | misconception
patterns_noticed: []
next_actions: []
---

## Session Summary
[What happened.]

## Key Moments
- Asked about: [X]
- Misconception surfaced: [if any]
- Connection made to: [other domain/concept]
- Struggled with: [if any]

## Suggested Next Actions
- [ ] Research: [topic]
- [ ] Practice: [drill]
- [ ] Review: [concept]
```

## Daily Note Format (for /obsidian-daily and reflection skill)

```yaml
---
created: YYYY-MM-DD
categories: [[daily-note]]
type: daily-note
---

# Daily Reflection — YYYY-MM-DD

## Summary
[Domains studied, topics covered.]

## Patterns Noticed
[Recurring themes from today's episodes.]

## Cross-Domain Connections
[Insights linking multiple domains.]

## Vault Health
- New notes created: N
- Raw sources processed: N
- Dangling links: [list]

## Tomorrow's Focus
[Suggested next area to study.]
```

## Skill-Specific Instructions

### For /obsidian-save
1. Extract decisions, insights, entities, learning moments from conversation
2. Create episode file in `vault/daily/` (NOT vault/wiki/)
3. Update existing wiki notes if new insight enriches them
4. Append new research topics to `vault/inbox.md`
5. Update `vault/log.md` with timestamp

### For /obsidian-ingest
1. Save original source to `vault/raw/` with research-source frontmatter
2. Scan existing vault notes for related concepts
3. Update related notes with new findings
4. Update `vault/_raw-index.md`

### For /obsidian-synthesize
1. Read `vault/_raw-index.md` for unprocessed sources (processed: false)
2. Create synthesized notes in `vault/[note-name].md` (flat root)
3. Set `processed: true` on source files
4. Create [[evergreen]] notes for cross-domain patterns
5. Update `vault/_master-index.md`

### For /obsidian-health
1. Scan for orphaned notes (no backlinks, not in index)
2. Find stale sources (>2yr old)
3. Detect contradictions between notes
4. Find dangling [[wiki-links]] → suggest research
5. Report to user

### For /obsidian-emerge
1. Read episodes from `vault/daily/` (last 30 days by default)
2. Identify recurring themes, misconceptions, patterns
3. Create [[evergreen]] notes for cross-domain patterns
4. Suggest research topics based on emergent curiosities

### For /obsidian-connect [A] [B]
1. Find notes for concept A and B
2. Draw parallels
3. Create or update [[evergreen]] connection note
4. Add cross-domain links to both source notes

### For /obsidian-world (Context Loading)
- L0 (minimal): learner name, current domain, current focus
- L1 (standard): + skill levels, equipment, persona, completed topics
- L2 (full): + partial topics, misconceptions, learning path, recent episodes
- L3 (exhaustive): + all vault content (synthesis/health tasks only)

Read `vault/learner-profile.md` for L0-L2. Scan vault for L3.

## Learner Profile

`vault/learner-profile.md` is the system anchor. **Only the `learning-profile` skill writes to it.** All other skills read it for context. Schema in `vault/templates/learner-profile-template.md`.

## Persona Presets

Conversational skills use tutor persona from learner-profile:
- `direct-mentor` — Efficient, no fluff
- `patient-coach` — Warm, encouraging
- `enthusiastic-peer` — High energy
- `dry-wit-professor` — Methodical, dry humor

Persona NEVER affects research or wiki content — always neutral.

## Background & Scheduled Agents

- **PostCompact hook**: After context compact → saves learnings, synthesizes raw, checks health
- **Morning 8 AM**: Daily briefing + study recommendations
- **Nightly 10 PM**: Reflection cycle (read episodes, extract patterns, create daily-note)
- **Weekly Friday 6 PM**: Week recap + cross-domain suggestions
- **Health Sunday 9 AM**: Full vault audit
