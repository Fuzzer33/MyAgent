# MyAgent — Personal Learning Second Brain

A Claude Code agent that researches real sources, builds you a personal knowledge base in Obsidian, and teaches you from it. Every conversation makes the system smarter.

## What This Does

Instead of just answering questions from general AI knowledge, this agent:

1. **Researches real sources** — searches the web, evaluates quality, cites everything
2. **Builds a knowledge base** — deposits findings into an Obsidian vault as linked wiki notes
3. **Teaches from YOUR notes** — the tutor references your actual knowledge base, not generic training data
4. **Remembers conversations** — every session is saved as an episodic record that feeds future learning
5. **Finds patterns** — nightly reflection detects what you keep struggling with, what connects across domains
6. **Adapts to you** — learns your equipment, goals, skill level, and preferred teaching style

## Quick Start (2 minutes)

### Prerequisites
- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) installed
- [Obsidian](https://obsidian.md) installed (free)

### Setup

1. **Open the vault in Obsidian:**
   Open Obsidian → "Open folder as vault" → select the `vault/` folder in this project

2. **Install Smart Connections plugin** (optional but recommended):
   Obsidian → Settings → Community plugins → Browse → "Smart Connections" → Install → Enable

3. **Start the agent:**
   ```bash
   cd MyAgent
   claude
   ```

4. **Just start talking.** The agent detects you're a new user and walks you through setup:
   - Your name and learning preferences
   - Pick a tutor persona (mentor, coach, peer, or professor)
   - Tell it what you want to learn and what you already know
   - It builds your learner profile and you're ready to go

## How to Use It

### In Claude Code (your conversation interface)

Just talk naturally. The agent figures out what you want:

| You say... | What happens |
|---|---|
| "Teach me about gain staging" | Tutor explains from your wiki notes |
| "Research sidechain compression" | Searches real sources, saves to vault |
| "Quiz me on EQ" | Tests your understanding from vault content |
| "What should I study next?" | Recommends based on your goals and progress |
| "Save this conversation" | Extracts insights into vault as episode notes |
| "What patterns do you see?" | Scans 30 days of sessions for recurring themes |
| "How does gain staging relate to photo exposure?" | Cross-domain connection analysis |
| "Check my vault health" | Audits for orphans, contradictions, stale notes |

### In Obsidian (your knowledge base)

Browse your growing knowledge base:
- **Category notes** (e.g., `audio-engineering.md`) — Dataview tables showing all related notes
- **Wiki notes** — Interconnected concept pages with `[[links]]` to everything
- **Daily notes** (`daily/`) — Session records and reflection summaries
- **Inbox** (`inbox.md`) — Topics queued for research
- **Graph view** — See how all your knowledge connects visually

### The Two Interfaces Work Together

```
You (Claude Code)          ←→          Your Knowledge (Obsidian)
                                       
"Teach me about EQ"        →   Reads vault/eq-fundamentals.md
                           →   Teaches from YOUR notes
"Save this"                →   Creates vault/daily/2026-04-09-eq-session.md
                                       
Tonight (automatic)        →   Reflection reads today's episodes
                           →   Creates daily summary
                           →   Detects: "keeps asking about EQ + compression"
                           →   Suggests: "study signal chain as a whole"
                                       
Tomorrow morning           →   Briefing recommends today's focus
You open Obsidian          →   New notes, updated indexes, fresh connections
```

## What Makes This Different From Just Asking Claude

| Just asking Claude | This agent |
|---|---|
| Answers from training data | Searches real sources, cites URLs |
| Every conversation starts fresh | Remembers your history, adapts over time |
| Generic advice | References YOUR equipment by name |
| No memory of what you've learned | Tracks completed topics, skill levels, misconceptions |
| Can't browse past learning | Full Obsidian vault with linked notes |
| Same answer for everyone | Adapts to your learning style and goals |

## Tutor Personas

During setup, you pick a teaching personality:

- **Direct Mentor** — "Here's the deal. Three things matter..."
- **Patient Coach** — "Let's take this step by step. How's that landing?"
- **Enthusiastic Peer** — "Okay this is actually really cool once it clicks!"
- **Dry-Wit Professor** — "Riveting topic, I know. But get this wrong and everything suffers."

The persona affects how the tutor talks to you, never the quality of research or content.

## Architecture (for the curious)

```
┌─────────────────────────────────────────────┐
│  You (Claude Code)                          │
│  "teach me about X" / "research Y" / etc.   │
└──────────────────┬──────────────────────────┘
                   │
         ┌─────────▼─────────┐
         │  Session Router    │  ← classifies intent
         └─────────┬─────────┘
                   │
    ┌──────────────┼──────────────┐
    ▼              ▼              ▼
┌────────┐  ┌──────────┐  ┌───────────┐
│ Tutor  │  │ Research  │  │ Vault Mgmt│
│        │  │ & Ingest  │  │ (obsidian-│
│ Teach  │  │           │  │  save,    │
│ Quiz   │  │ Search    │  │  health,  │
│ Drill  │  │ Evaluate  │  │  emerge,  │
│ Review │  │ Deposit   │  │  etc.)    │
└───┬────┘  └─────┬─────┘  └─────┬─────┘
    │             │              │
    ▼             ▼              ▼
┌─────────────────────────────────────────────┐
│  Obsidian Vault (Kepano-style Zettelkasten) │
│                                             │
│  wiki notes / raw sources / daily episodes  │
│  references / categories / evergreen notes  │
│  learner-profile / inbox / indexes          │
└─────────────────────────────────────────────┘
    │                                    ▲
    │  Nightly reflection cycle          │
    │  (reads episodes, extracts         │
    │   patterns, updates vault)         │
    └────────────────────────────────────┘
```

## Project Structure

```
MyAgent/
├── .claude/skills/        — 7 learning agent skills (the brain)
├── vault/                 — Obsidian knowledge base (the memory)
│   ├── templates/         — Note templates
│   ├── references/        — Tool/equipment reference notes
│   ├── raw/               — Unprocessed research sources
│   ├── daily/             — Session episodes + daily reflections
│   └── *.md               — Wiki notes, indexes, learner profile
├── scripts/               — Background maintenance scripts
├── docs/                  — Design specs and plans
└── CLAUDE.md              — Agent instructions (for Claude, not humans)
```

## Credits

- Built with [Claude Code](https://docs.anthropic.com/en/docs/claude-code) skills
- Vault management by [obsidian-second-brain](https://github.com/eugeniughelbur/obsidian-second-brain) (eugeniughelbur)
- Knowledge base structure inspired by [Steph Ango's Kepano system](https://stephango.com/)
- RAG via [Smart Connections](https://github.com/brianpetro/obsidian-smart-connections) plugin
