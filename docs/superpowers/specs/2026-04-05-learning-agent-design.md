# Learning Agent — Design Specification

> **Project:** Personalized Research-First Learning Agent
> **Course:** AI Agents (Spring 2026, UMaine)
> **Author:** Alex Sharon
> **Date:** 2026-04-05
> **Status:** Approved Design

---

## 1. Overview

A Claude Code skills-based agent that autonomously researches topics, builds an Obsidian Zettelkasten knowledge base, and tutors the user from that grounded knowledge — not from general LLM training data. Designed for multidisciplinary learners who want to reduce the synthesis overhead of self-directed learning across multiple fields.

**Core value proposition:** The agent searches, filters, organizes, and synthesizes real-world sources so the user can focus on understanding and building, not on hunting for information.

**Prototype scope:** One working domain (FL Studio / music production) for the class demo. Architecture is domain-agnostic from day one — adding new domains requires only updating the learner profile and queuing research.

---

## 2. Key Design Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Vault architecture | Dual vault — hard separation | Agent vault lives inside the project directory. User's personal Obsidian vault is never referenced, never accessed, never known to the agent. Non-negotiable security boundary. |
| Vault structure | Kepano-style Zettelkasten | Flat root, properties and links organize (not folders), composable templates, references folder, rating 1-7. Follows the system described by Steph Ango (Obsidian CEO). |
| Tutor fallback | Labeled general knowledge + nightly research prompt | When wiki doesn't cover a topic: give a labeled answer ("this is from general knowledge, not researched sources"), then prompt "Want me to add this to tonight's research queue?" |
| Research autonomy | Plan-then-execute | Agent generates a research plan from `inbox.md` topics + prerequisite/adjacent knowledge. User approves before overnight execution. |
| Conflicting sources | Recommend consensus, note alternatives | Present the community-adopted approach as the recommendation with evidence. Note alternatives with attribution. Accuracy is critical — multiple sources must agree before making a recommendation. |
| Persona depth | Two-tier | Persona colors conversation (session-router, tutor). Research-and-ingest and wiki-builder produce neutral, objective reference material. |
| Running questions list | `inbox.md` — dual input | User jots topics in Obsidian directly. Agent also appends during sessions (fallback flow). Single file, two entry points. |
| Technical architecture | Pure Claude Code Skills | No MCP server, no vector database, no embeddings. Skills as markdown prompts in `.claude/skills/`. Vault is plain markdown navigated via Karpathy-style index files. |

---

## 3. Design Philosophy

### 3.1 Research-first, not knowledge-first

The agent's primary mode: search first, retrieve real sources, then synthesize from those sources with citations. It never defaults to answering from general LLM knowledge when it could find the actual community consensus.

### 3.2 Source quality as a first-class concern

```
Tier 1 (prefer):      Official documentation, manufacturer specs
Tier 2 (good):        High-upvote community posts, widely-cited tutorials,
                       active GitHub repos (stars, recent commits)
Tier 3 (use caution): Blog posts, single-source claims
Reject:               SEO spam, outdated docs (>2yr for software),
                       abandoned repos, no community validation
```

Every claim gets a confidence label:
- **Well-established** — multiple quality sources agree
- **Community consensus** — widely upvoted/adopted, not in official docs
- **Single source** — only one source, flagged
- **Agent inference** — agent connected dots between sources, clearly labeled

### 3.3 Obsidian-native Zettelkasten (Kepano system)

The knowledge base lives as structured markdown in Obsidian. Not a vector database, not opaque. The user can see, browse, and edit everything.

Organizational principles (from Steph Ango's system):
- **Minimal folders** — most notes live in the vault root
- **Categories are properties, not folders** — category notes with Dataview base tables auto-list related notes
- **Properties use links** — `categories: [[audio-engineering]]` not `categories: audio-engineering`
- **Composable templates** — a note can have multiple templates stacked (concept + tool-guide)
- **Link first mentions liberally** — even to notes that don't exist yet (sets research targets)
- **Rating 1-7** — how essential a concept is, applicable to any note
- **File over app** — markdown files outlast any software
- **Speed and laziness** — minimize overhead of deciding where things go
- **References folder** — for things outside your world (tools, plugins, people, books)

Navigation: Karpathy-style index files for cheap traversal by the agent. User navigates via Quick Switcher (Ctrl+O), category base tables, and backlinks.

### 3.4 Designed for multidisciplinary learning

The flat Zettelkasten structure means a note on gain staging can link to data normalization. Cross-domain connections are a core feature. The `domains` property on notes (using linked categories) allows the same note to belong to multiple fields. Category base tables surface these intersections.

### 3.5 Tone and persona

Customizable tutor persona applied to conversational skills only. Four presets:
- **The Mentor** — Direct, experienced, doesn't waste time. "Here's what you need to know."
- **The Coach** — Warm, patient, checks in. Good for domains where the user feels insecure.
- **The Peer** — Enthusiastic, fellow-learner energy. Makes learning feel fun.
- **The Professor** — Structured, methodical, dry humor. Good for theoretical domains.

Persona never affects research or wiki content — those stay neutral and objective.

---

## 4. Vault Structure

```
vault/
|-- templates/
|   |-- concept.md              # Core idea / technique (composable)
|   |-- tool-guide.md           # Software/hardware guide (composable)
|   |-- workflow.md             # Step-by-step process (composable)
|   |-- exercise.md             # Practice drill (composable)
|   |-- lesson.md               # Generated lesson sequence
|   |-- evergreen.md            # Reusable insight (Kepano-style)
|   |-- research-source.md      # Raw source deposit
|   |-- category.md             # Category note with base table
|   |-- weekly-review.md        # Learning review
|
|-- references/                  # Things "outside your world"
|   |-- (tools, plugins, people, books, courses...)
|
|-- attachments/                 # Images, PDFs, etc.
|
|-- raw/                         # Research staging area (source-per-file)
|   |-- (source files from research-and-ingest)
|
|-- daily/                       # Daily notes (date-linked)
|
|-- _master-index.md             # Auto-maintained nav index
|-- _raw-index.md                # Index of unprocessed sources
|-- inbox.md                     # Running questions/topics list
|-- learner-profile.md           # Persistent learner state
|
|-- (category notes in root...)  # e.g. audio-engineering.md, photography.md
|-- (synthesized notes in root.) # e.g. sidechain-compression.md
|-- (evergreen notes in root...) # e.g. gain-staging-is-normalization.md
|-- (lesson sequences...)        # e.g. vocal-mixing-lesson-1.md
```

### 4.1 Note template — synthesized wiki note

```yaml
---
created: {{date}}
categories: [[domain-category]]
tags: []
type: concept                    # concept | technique | tool-guide | workflow | exercise
difficulty: beginner             # beginner | intermediate | advanced
rating:                          # 1-7 (Kepano-style, how essential)
sources: []                      # links to raw/ source files
prerequisites: []                # [[wiki-links]] to prerequisite notes
---

Content. Liberal use of [[wiki-links]] to other notes.
Link first mentions of any concept, tool, or technique.

## Sources
- [Source Title](url) -- retrieved {{date}}
```

### 4.2 Note template — research source

```yaml
---
created: {{date}}
categories: [[research-source]]
source_url:
source_type:                     # documentation | tutorial | forum | paper | video
quality_tier:                    # 1 | 2 | 3
confidence:                      # well-established | community-consensus | single-source
domain:
tags: []
processed: false                 # flips to true when wiki-builder synthesizes it
---

## Key Findings

(Paraphrased, not copied. Every claim attributed.)

## Relevance

(Why this source matters for the learning goal.)

## Equipment-Specific Notes

(Anything specific to the user's gear, if applicable.)
```

### 4.3 Note template — category

```yaml
---
created: {{date}}
categories: [[category]]
tags: []
---

# {{Category Name}}

```dataview
TABLE difficulty, rating, type
FROM ""
WHERE contains(file.frontmatter.categories, this.file.link)
SORT rating DESC
```
```

### 4.4 Note template — reference

```yaml
---
created: {{date}}
categories: [[reference]]
type:                            # tool | plugin | person | book | course | hardware
tags: []
url:
rating:
---

(Description, key details, how it relates to the user's setup.)
```

### 4.5 Note template — evergreen

```yaml
---
created: {{date}}
categories: [[evergreen]]
tags: []
rating:
---

(A reusable insight or principle that connects across domains.)
```

### 4.6 Note template — lesson

```yaml
---
created: {{date}}
categories: [[lesson]]
domain:
lesson_number:
topic:
difficulty:
prerequisites: []
covers: []                       # [[wiki-links]] to concepts taught
---

(Structured lesson content generated from wiki notes.)
```

### 4.7 Learner profile schema

```yaml
---
name: Alex
created: 2026-04-06

learning_style:
  input_mode: verbal-stream
  conceptual_approach: big-picture-first
  learning_mode: build-then-learn
  analogy_preference: cross-domain
  overwhelm_sensitivity: high
  momentum_style: burst

tutor_persona:
  name: "Jarvis"
  personality: direct-mentor     # direct-mentor | patient-coach | enthusiastic-peer | dry-wit-professor
  verbosity: concise             # concise | moderate | detailed
  celebrate_progress: true
  use_cross_domain_analogies: true

domains:
  - name: "[[audio-engineering]]"
    skill_level: beginner
    equipment: ["[[Volt 476]]", "[[AT2035]]", "[[FL Key 37]]", "[[FL Studio]]"]
    goals: [live mixing, vocal recording, basic mastering]
    completed_topics: []
    current_focus: null
    queued_topics: []
  - name: "[[photography]]"
    skill_level: beginner
    equipment: ["[[Fujifilm X-T4]]", "[[Capture One Pro]]"]
    goals: [portrait editing, color grading, professional output]
    completed_topics: []
    current_focus: null
    queued_topics: []
  - name: "[[knowledge-management]]"
    skill_level: intermediate
    equipment: ["[[Obsidian]]"]
    goals: [Dataview mastery, automation, MIDI integration]
    completed_topics: [basic vault setup, YAML frontmatter, tags]
    current_focus: Dataview queries
    queued_topics: []

last_updated: 2026-04-06
---
```

---

## 5. Skills Architecture

All skills live in `.claude/skills/` as markdown skill files. Claude Code loads them as system prompts when invoked.

### 5.1 `session-router`

**Purpose:** Entry point for all interactions. Classifies intent and routes to the appropriate skill.

**Routing table:**

| Intent pattern | Routes to | Context passed |
|---|---|---|
| "I want to learn about X" / "Research X" | `research-and-ingest` | topic, domain, equipment |
| "Teach me X" / "Explain X" / "Quiz me" | `tutor` | topic, skill level, persona |
| "What should I study next?" / "Update progress" | `learning-profile` | session results |
| "Build a lesson on X" / "Synthesize raw notes" | `wiki-builder` | topic, available raw sources |
| Ambiguous / conversational | Ask one clarifying question, then route | -- |

**Behavior:**
- Reads `learner-profile.md` at session start for full context
- Loads `tutor_persona` and applies persona tone to its own routing messages
- Handles messy, stream-of-consciousness input — extracts intent without asking to rephrase
- Passes equipment context to downstream skills
- Never answers directly — always routes through a skill

### 5.2 `research-and-ingest`

**Purpose:** Given a learning goal, autonomously searches for high-quality real sources and deposits structured markdown into `raw/`.

**Workflow:**
1. Read topic/questions from input or `inbox.md`
2. Read `learner-profile.md` for equipment context and skill level
3. Decompose topic into research subtasks
4. Expand with prerequisite/adjacent knowledge the user might not know to ask about
5. Present research plan for user approval
6. For each subtask: search using web search tools
7. Evaluate each source against quality tiers (Section 3.2)
8. Create a `raw/` file per quality source using `research-source` template
9. Update `_raw-index.md`
10. Mark completed items in `inbox.md`

**Critical rules:**
- Never synthesize from general LLM knowledge — every claim traces to a retrieved source
- Prefer official documentation and widely-adopted community resources
- Include source URL for every piece of information
- Apply confidence labels to every claim
- Reject low-quality sources (SEO spam, outdated, abandoned)
- Accuracy is paramount — multiple sources must agree before stating something as consensus

**Overnight candidate:** This skill + wiki-builder form the `/schedule` overnight pipeline.

### 5.3 `wiki-builder`

**Purpose:** Takes raw research from `raw/` and synthesizes it into Kepano-style Zettelkasten notes.

**Workflow:**
1. Read `_raw-index.md` to find unprocessed sources (`processed: false`)
2. Group related sources by domain/topic
3. Synthesize into vault notes using composable templates
4. Link liberally — first mention of any concept, tool, or technique gets `[[wiki-linked]]`
5. Create reference notes in `references/` for tools, plugins, people
6. Create or update category notes in root with Dataview base tables
7. Update `_master-index.md`
8. Mark source files as `processed: true`
9. Append dangling links (notes that don't exist yet) to `inbox.md` as research suggestions

**Synthesis rules:**
- Build from `raw/` sources only — never general LLM knowledge
- Stack composable templates where appropriate
- Include "what people actually do" callouts with adoption evidence
- Conflicting sources: recommend consensus, note alternatives with attribution
- Cross-domain links are a priority — actively create connections between fields
- Rate 1-7 based on how essential the concept is to the user's goals
- Calibrate difficulty to learner profile

**Output voice:** Neutral, objective reference material. No persona applied.

### 5.4 `tutor`

**Purpose:** Interactive teaching grounded in the knowledge base. Persona-driven.

**Modes:**

| Mode | Trigger | Behavior |
|---|---|---|
| Explain | "Explain X" / "Walk me through X" | Teach from wiki. Big picture first, then details. Reference `[[pages]]`. |
| Quiz | "Quiz me on X" | Generate questions from wiki content. Test understanding, not memorization. |
| Drill | "Give me practice for X" | Equipment-specific hands-on tasks. "On your Volt 476, do X..." |
| Clarify | "What's the difference between X and Y?" | Short, targeted answer. Minimum to unblock. |
| Connect | "How does X relate to Y?" | Cross-domain linking and analogies. |

**Persona application:**
- Load `tutor_persona` config from `learner-profile.md`
- Adjust tone, verbosity, analogy style, question frequency
- Persona presets: direct-mentor, patient-coach, enthusiastic-peer, dry-wit-professor

**Fallback behavior:**
1. If topic not in wiki, give labeled answer: "This is from my general knowledge, not from researched sources."
2. Prompt: "Want me to add this to tonight's research queue? I'll build a proper wiki entry with real sources."
3. If yes, append to `inbox.md`

**Critical rules:**
- Read relevant wiki notes before teaching — cite which `[[page]]` info comes from
- Read `learner-profile.md` for skill level, equipment, learning style
- Equipment-specific always — "on your Volt 476" not "on your audio interface"
- Big-picture first, details second
- Socratic check-ins at persona-configured frequency
- Never re-explain topics listed in `completed_topics`
- When user demonstrates understanding, request progress update via learning-profile skill

### 5.5 `learning-profile`

**Purpose:** Maintains persistent learner state. Single source of truth across sessions.

**Capabilities:**
- **Status overview** — Recommend highest-value next topic based on goals, prerequisites, and available wiki content
- **Progress updates** — Move topics from `current_focus` to `completed_topics`, advance `skill_level` at milestones
- **Next-step recommendation** — Always one clear next step with rationale, plus 2-3 alternatives. Never a list of 47 things.
- **Cross-domain suggestions** — Surface connections when completing a topic that has analogues in another domain
- **New domain onboarding** — Create domain entry, ask about equipment/goals, queue initial research to `inbox.md`
- **Momentum protection** — Track active domains. Feed momentum when on a streak. Gently surface dormant domains without guilt.

**Critical rules:**
- Every skill reads `learner-profile.md` at session start
- Only this skill writes to `learner-profile.md` (other skills request updates via routing)
- Properties use `[[links]]` for Obsidian navigability
- `completed_topics` is append-only — never removes progress
- Skill level changes require demonstrated understanding, not just reading

---

## 6. The Overnight Pipeline

### 6.1 Evening

1. Throughout the day, user jots topics into `inbox.md` (in Obsidian or via tutor fallback prompts)
2. Before bed, user runs the agent
3. Session-router sees pending inbox items, routes to `research-and-ingest`
4. Research-and-ingest reads `inbox.md` + `learner-profile.md`, generates research plan (user's topics + prerequisite/adjacent knowledge)
5. User reviews plan, tweaks, approves
6. User runs `/schedule` for overnight execution

### 6.2 Overnight (autonomous)

1. `research-and-ingest` executes the approved plan — searches, evaluates, deposits into `raw/`
2. `wiki-builder` picks up new `raw/` files — synthesizes into vault notes, creates references, links everything, updates indexes
3. `wiki-builder` appends suggested follow-up topics to `inbox.md` (dangling links, prerequisite gaps)
4. `learning-profile` updates `queued_topics` and `current_focus` based on new content

### 6.3 Morning

1. User opens Obsidian, browses new notes via Quick Switcher or category base tables
2. New wiki notes, reference notes, and category updates are ready
3. `inbox.md` shows completed items and new suggestions
4. User can start a tutoring session on any new material immediately

### 6.4 Class demo strategy

Pre-build a wiki batch as if the overnight pipeline ran (FL Studio mixing domain). Demo the tutor interacting with that content live. The pipeline concept is explained with `inbox.md` -> `raw/` -> wiki flow visible as artifacts. Live run of research-and-ingest on one small topic if time permits.

---

## 7. Test Personas

### Persona 1: Alex (primary)
- CS/Math double major, entering Data Science master's
- Beginner in music production and photo editing
- Equipment: Volt 476, AT2035, FL Key 37, FL Studio, Fujifilm X-T4, Capture One Pro
- Learning style: verbal-stream, big-picture-first, build-then-learn, cross-domain analogies
- Success: wakes up to well-organized wiki, feels learning is manageable

### Persona 2: Priya (graduate researcher)
- Statistics PhD, textbook-strong, struggles with practical application
- Equipment: R Studio, Python/pandas, HPC cluster
- Success: agent finds practical examples of her specific method applied to similar datasets

### Persona 3: Marcus (career changer)
- Former accountant learning web dev, zero programming background
- Equipment: MacBook Air, VS Code
- Success: agent identifies the ONE stack bootcamp grads actually use, explains without jargon

### Persona 4: Jordan (experienced dev, new domain)
- 5 years backend engineering, learning ML/data science
- Equipment: Linux workstation, Docker, Python expert
- Success: agent maps ML concepts to software engineering analogies, skips basics

---

## 8. Success Criteria

1. A classmate can interact with the agent and understand the value proposition within 2 minutes
2. The tutor teaches from the knowledge base, not general knowledge — visibly different from just asking Claude
3. The overnight pipeline concept is clear even with pre-built demo content
4. Source quality filtering is visible — agent explains why it chose certain sources
5. Personalization is visible — references specific equipment, adjusts to skill level
6. Alex personally finds the output useful for an actual learning goal
7. Tutor persona affects interaction tone noticeably — switching personas changes the experience
8. Agent handles messy, spoken-style input gracefully
9. Using the agent feels enjoyable, not like a chore
10. Learning feels manageable — clear next steps, chunked material, progress markers

---

## 9. Future Directions (Post-Prototype)

### Voice layer
- Full Jarvis mode: MIDI pad triggers STT (Handy/Whisper) -> agent -> TTS (Kokoro) response
- Voice-guided walkthroughs while working in FL Studio or Capture One
- Multiple tutor voices for different domains
- NotebookLM-style audio lessons from wiki content

### Knowledge expansion
- Spaced repetition / Anki card generation from wiki content
- Practice drill generator calibrated to skill level
- Learning velocity tracker across domains
- Community source monitor (subreddits, YouTube channels, forums)
- Teach-back mode: user explains concept back, agent evaluates gaps

### Technical
- MCP server for structured vault operations if index-file navigation hits scale limits
- Multi-agent pipeline: separate research, synthesis, and teaching agents with handoff
- Export to other formats: podcast scripts, slide decks, checklists

---

## 10. Technical Stack

| Component | Tool | Notes |
|---|---|---|
| Agent framework | Claude Code Skills (`.claude/skills/`) | Required by class |
| LLM | Claude (via Claude Code) |
| Search/retrieval | Claude Code web search | Tavily for production |
| Knowledge base | Obsidian vault (markdown) | Kepano-style Zettelkasten |
| Overnight automation | Claude Code `/schedule` | Queue research tasks |
| Version control | Git + GitHub | Required by class |
| Note structure | YAML frontmatter + wiki-links | Composable templates, categories as properties |
| TTS (future) | Kokoro TTS | Open source, local, multi-voice |
| STT (future) | Handy (Whisper/Parakeet) | System-wide dictation |
| Voice trigger (future) | Bome MIDI Translator Pro + FL Key 37 | Existing infrastructure |
