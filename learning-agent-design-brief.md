# AI Learning Agent — Design Brief & Brainstorming Document

> **Project:** Personalized Research-First Learning Agent  
> **Course:** AI Agents (Spring 2026, UMaine)  
> **Author:** Alex Sharon  
> **Date:** April 5, 2026  
> **Status:** Brainstorming / Pre-Prototype

---

## 1. The Problem This Agent Solves

I'm a CS and Math double major entering a Data Science & Engineering master's program. Outside of academics, I have a growing list of technical skills I want to develop — music production in FL Studio, photo editing in Capture One Pro, Obsidian-based knowledge management, and more. Each one of these is a deep domain with its own ecosystem of tools, techniques, and community knowledge.

The core pain point is **synthesis overhead**. The information exists — scattered across YouTube tutorials, forum threads, official documentation, Reddit posts, GitHub repos — but the work of finding it, filtering for quality, organizing it, and building a coherent mental model takes longer than the actual learning. This overhead is draining and creates a constant sense of being behind, which lowers quality of life and blocks the enjoyment I'd get from these projects.

### What existing tools fail to do

- **Claude Chat / ChatGPT / general LLMs**: Respond from latent training knowledge. This leads to plausible-sounding but sometimes inaccurate or outdated answers. They suggest solutions that *could* work but aren't what people actually use. They have no memory across sessions, no persistent knowledge base, and no ability to do autonomous research.
- **NotebookLM (Google)**: Excellent at grounded synthesis — it works from documents you provide, not hallucinated knowledge. But it's manual (you feed it docs yourself), not agent-based (no autonomous research loop), and not personalized to your equipment/skill level/goals.
- **Perplexity / search-augmented chat**: Does real-time search but gives one-shot answers, not structured learning paths. No persistence, no personalization, no overnight research capability.
- **Traditional RAG systems**: Powerful but heavy — vector databases, embeddings, retrieval pipelines. Overkill for a solo learner. Hard to inspect what's actually in the knowledge base.

### What an agent can do that none of these can

The key agent capabilities that matter here:

1. **Autonomy** — I give it a learning goal, it plans and executes multi-step research without me sitting there prompting back and forth.
2. **Persistence** — It builds a knowledge base that grows over time. It remembers what I've already learned.
3. **Grounding** — It teaches from retrieved, real-world sources — not from its own latent knowledge. When it recommends a tool or technique, it's because real people actually use it.
4. **Personalization** — It knows my equipment (Fujifilm X-T4, Volt 476 audio interface, FL Key 37, FL Studio, Capture One Pro), my current skill level, and what I've already covered. It doesn't re-explain things I already know.
5. **Overnight operation** — Using Claude Code's `/schedule` command, I can queue research and synthesis tasks that run while I sleep. I wake up to structured learning materials, not a blank page.

---

## 2. Core Design Philosophy

### 2.1 Research-first, not knowledge-first

The agent's primary mode should be: **search first, retrieve real sources, then synthesize from those sources with citations.** It should never default to answering from general LLM knowledge when it could instead find what the actual community consensus is.

**Practical implication:** When I ask "how do I sidechain compress in FL Studio," the agent should NOT just explain sidechain compression from training data. It should search for the most-used FL Studio sidechain techniques, find which plugins people actually use, check the FL Studio documentation, and synthesize a grounded answer that reflects real practice.

### 2.2 Source quality as a first-class concern

Not all sources are equal. The agent should have explicit quality criteria:

- **Prefer official documentation** over blog posts over forum answers
- **Prefer open-source tools** with high GitHub stars, active maintenance, good docs
- **Prefer community-validated approaches** (highly upvoted answers, widely-used workflows)
- **Prefer recent sources** for fast-moving domains (software tools, AI/ML)
- **Flag when information is the agent's own synthesis** vs. directly from a source
- **Avoid obscure or hallucinated solutions** — if a tool or technique doesn't have clear community adoption, say so

### 2.3 Obsidian-native knowledge graph (Karpathy/Kepano hybrid)

The knowledge base should live in Obsidian as structured markdown — not in a vector database, not in an opaque system. This gives two major benefits:

1. **Transparency** — I can see, browse, and edit everything the agent has researched. It's not a black box.
2. **Integration** — The agent's output lives in the same ecosystem as my personal notes. I can pull agent-generated notes into my personal vault when I've internalized them.

The architecture combines:

- **Karpathy's approach**: `raw/` staging folder → wiki synthesis → index files for cheap traversal. Claude Code navigates via index files rather than expensive recursive file searches.
- **Kepano's approach**: YAML frontmatter properties as schema, categories as organizing principle, wiki-links between concepts, composable templates for different note types, minimal folder structure (let links and properties do the organizing).

### 2.4 Dual-vault separation

Two distinct spaces:

| | AI Vault (agent workspace) | Personal Vault (my notes) |
|---|---|---|
| **Who writes here** | The agent | Me |
| **What lives here** | Research, synthesized wikis, generated lessons, learning paths | Journal entries, my own notes, things I've internalized |
| **Agent access** | Full read/write | Read-only (NEVER modify, especially daily notes) |
| **Review flow** | I review agent output → drag/move notes I want to keep into my personal vault | Agent can reference my learning profile and progress but never edit |

This protects my personal knowledge system while giving the agent a structured workspace.

### 2.5 Tone and collaboration style

- **Direct and practical**, not academic or hand-holdy
- **"Here's what people actually do"** energy — like getting advice from a knowledgeable coworker, not a textbook
- **Socratic when appropriate** — ask questions to gauge understanding before dumping information
- **Honest about uncertainty** — if the agent isn't sure what the community standard is, it says so rather than guessing
- **Respects my time** — concise explanations, clear action items, links to sources for deeper reading
- **Calibrates to skill level** — doesn't over-explain basics I already know, doesn't skip fundamentals I'm missing

### 2.6 Voice & personality layer — the "Jarvis" concept

Learning from a wall of text is fundamentally different from learning from a person who talks to you. This agent should feel more like a knowledgeable human tutor than a search engine that returns paragraphs. The vision is something closer to Iron Man's Jarvis — an always-ready, personalized assistant with a distinct voice and personality that makes interacting with it feel natural and even enjoyable.

**Why this matters for learning specifically:**

- **Auditory processing**: Some concepts stick better when heard than when read, especially for procedural skills ("now bring the fader down to about -6dB, you'll hear the vocal sit right into the mix")
- **Engagement and momentum**: A voice personality creates a sense of a relationship with the tutor. This isn't about pretending AI is human — it's about reducing the friction and loneliness of self-directed learning.
- **Multitasking**: If I'm learning FL Studio mixing techniques, I want to hear instructions while my hands are on the controls — not alt-tab to read a text wall.
- **Personality as a design surface**: A tutor who's enthusiastic about the subject, slightly irreverent, and treats the learner as a peer creates a fundamentally different learning experience than a neutral information-delivery system.

**Customizable tutor persona:**

The `learner-profile.md` should include a `tutor_persona` configuration:

```yaml
tutor_persona:
  name: "Jarvis"                     # or whatever the user wants to call it
  personality: direct-mentor          # options: patient-coach, direct-mentor, enthusiastic-peer, dry-wit-professor
  voice: british-male                 # Kokoro TTS voice selection
  quirks:
    - occasionally uses music analogies when explaining CS concepts
    - calls the user by first name
    - celebrates milestones without being cheesy
  communication_style:
    verbosity: concise                # concise | moderate | detailed
    question_frequency: moderate      # how often to check understanding
    analogy_preference: cross-domain  # use analogies from user's other interests
```

**Personality presets (users can customize or start from one):**

- **"The Mentor"** — Direct, experienced, doesn't waste your time. Says things like "Here's what you need to know" and "Skip that, it doesn't matter for what you're doing." British accent optional but encouraged for the Jarvis feel.
- **"The Coach"** — Warm, patient, checks in on how you're feeling about the material. Good for domains where the user feels insecure or overwhelmed.
- **"The Peer"** — Enthusiastic, talks like a fellow student who's just slightly ahead of you. Uses "dude, wait till you see this" energy. Good for making learning feel fun rather than like work.
- **"The Professor"** — Structured, methodical, dry humor. Gives context and history before the practical. Good for theoretical/mathematical domains.

**Technical implementation (Kokoro TTS):**

- **Tool**: Kokoro TTS — open source, runs locally, supports multiple voices, 17k+ GitHub stars
- **Pipeline**: Agent generates text response → text is piped to Kokoro → audio plays through system speakers or headphones
- **Trigger**: MIDI pad press via Bome MIDI Translator Pro (existing infrastructure). Pad 15 on the FL Key 37 could be the "talk to tutor" button.
- **Session flow**: Press pad → system listens (via Whisper/Handy for STT) → agent processes → Kokoro speaks the response → user responds or presses pad again
- **Fallback**: Text-only mode always available. Voice is additive, not required.

**For the class prototype:** The voice layer is a strong future direction but not the core deliverable. For the prototype, implement the personality system in text (different system prompts per persona) and document the voice pipeline as a planned feature with Kokoro as the specific tool. If there's time, a short demo of one response piped through Kokoro would be impressive but not essential.

### 2.7 Designed for Alex — learning style analysis

This agent is being built by me, for me (and others like me), so the design should reflect how I actually learn. Based on self-reflection and how I naturally approach problems:

**How I think and communicate:**

- **Stream-of-consciousness / verbal processor**: I think by talking (or dictating). My best ideas come out as long, flowing, associative chains — not as structured outlines. The agent should be comfortable with messy, rambling input and be good at extracting the core question or intent from a wall of spoken text.
- **Big-picture first, then details**: I need to understand the conceptual landscape before I can absorb specifics. "Here's the whole domain, here's where this technique fits in it, now here's the technique" — not "step 1, step 2, step 3" without context.
- **Integrative / cross-domain thinker**: I naturally draw connections between different fields — music theory and math, signal chains and data pipelines, MIDI automation and productivity systems. The agent should actively make these connections rather than treating each learning domain as isolated.
- **Learns by building**: I don't learn by reading documentation end-to-end. I learn by trying to build something, hitting a wall, and then looking up exactly what I need. The agent should support this — "you're trying to do X, here's the specific thing you need to know right now" rather than "here's a comprehensive overview of the entire topic."

**What motivates and drains me:**

- **Motivation**: Seeing tangible progress. Having something work. The moment where a concept clicks and I can do a new thing. Cross-domain "aha" moments.
- **Drain**: The feeling of being buried under too many things to learn. Spending an hour searching for information and not finding a clear answer. Getting generic advice that doesn't apply to my specific setup.
- **Momentum**: I work in bursts of high focus. When I'm excited about something, I can go deep for hours. But if the friction is too high (can't find the info, agent is being unhelpful, too much setup required), I lose steam fast.

**Design implications for the agent:**

1. **Accept messy input gracefully**: The session-router should handle long, spoken, stream-of-consciousness messages and extract intent without asking the user to rephrase. Don't punish the user for being verbose.

2. **Always provide the map before the territory**: When teaching a new concept, start with "here's where this fits in the bigger picture" before diving into details. Use the wiki's index structure to show context.

3. **Cross-domain analogies are a feature, not a gimmick**: The agent should know enough about all of the user's domains to draw connections. "Gain staging in audio is like normalization in data science — you're making sure your signal is in the right range before processing." These should come up naturally, not be forced.

4. **Support the "build-first, learn-as-needed" cycle**: When the user says "I'm trying to do X and I'm stuck," the agent should give the minimum necessary explanation to unblock them, with links to deeper material if they want it later. Don't lecture when they need a quick answer.

5. **Chunk the overwhelm**: Never present the full scope of what there is to learn without also presenting a clear "start here, then this, then that" sequence. The learning profile should always have a clear "next step" — not a list of 47 things to eventually get to.

6. **Celebrate momentum**: When the user completes a topic or demonstrates understanding, acknowledge it concretely. "You've now covered the three core EQ techniques — that's the foundation for everything else in mixing." Not fake enthusiasm, just clear markers of progress.

7. **Low friction above all else**: If using the agent requires more setup, configuration, or cognitive overhead than just Googling, it's failed. The MIDI pad trigger, the overnight pipeline, the pre-built wiki — these all exist to reduce friction to near zero.

8. **Don't make the user repeat context**: The learning profile exists so the agent never asks "what equipment do you have?" twice. Every session should feel like a continuation, not a cold start.

---

## 3. Agent Architecture — Skills Design

### Skill 1: `session-router`

**Purpose:** Entry point for all interactions. Classifies user intent and routes to the appropriate skill.

**Intent categories:**
- "I want to learn about X" → `research-and-ingest`
- "Build me a lesson/wiki on X" → `wiki-builder`
- "Teach me / quiz me / explain X" → `tutor`
- "What should I study next?" → `learning-profile`
- "Update my skill level on X" → `learning-profile`
- Ambiguous / conversational → Ask clarifying questions before routing

**Critical rules:**
- Always confirm the domain/topic before routing to research
- If the user mentions specific equipment or tools, pass that context to the downstream skill
- Never skip routing and try to answer directly — the whole point is grounded, skill-mediated responses

### Skill 2: `research-and-ingest`

**Purpose:** Given a learning goal, autonomously search for high-quality real sources and deposit structured markdown into the AI vault's `raw/` folder.

**Workflow:**
1. Parse the learning goal into specific research subtasks
2. For each subtask, search for sources using web search (Tavily in production, Claude Code web search for prototype)
3. Evaluate each source against quality criteria (see §2.2)
4. For each quality source, create a structured markdown file in `raw/` with:
   - YAML frontmatter: `source_url`, `source_type` (documentation/tutorial/forum/paper), `quality_score`, `date_retrieved`, `domain`, `tags`
   - Extracted key information (paraphrased, not copied)
   - Links to related concepts
5. Update the raw index file

**Critical rules:**
- NEVER synthesize from general LLM knowledge — every claim must trace to a retrieved source
- Prefer official documentation and widely-adopted community resources
- Include the source URL for every piece of information
- Flag confidence level: "well-established" vs. "one source says" vs. "agent inference"
- Do not ingest low-quality sources (SEO spam, outdated docs, abandoned repos)

**This is the overnight `/schedule` candidate.** User queues topics before bed, this skill runs autonomously.

### Skill 3: `wiki-builder`

**Purpose:** Takes raw research from the `raw/` folder and synthesizes it into structured wiki notes following Kepano's organizational principles.

**Output structure:**
```
ai-vault/
├── wiki/
│   ├── _master-index.md          # List of all wikis
│   ├── fl-studio-mixing/
│   │   ├── _index.md             # Overview + links to all pages in this wiki
│   │   ├── sidechain-compression.md
│   │   ├── eq-fundamentals.md
│   │   └── gain-staging.md
│   ├── capture-one-portraits/
│   │   ├── _index.md
│   │   ├── color-grading.md
│   │   └── skin-retouching.md
│   └── ...
├── raw/                          # Staging area (research deposits)
├── lessons/                      # Generated lesson sequences
└── learner-profile.md            # Persistent learning state
```

**Each wiki page should have:**
- YAML frontmatter: `categories`, `tags`, `created`, `sources`, `difficulty`, `prerequisites`
- Wiki-links (`[[concept]]`) to related concepts within and across wikis
- "What people actually use" callouts — concrete tool/plugin/technique recommendations with adoption evidence
- "Sources" section at the bottom with links to original materials

**Critical rules:**
- Build wiki from `raw/` sources, not from general knowledge
- Use Kepano-style composable templates — a note can be both a `technique` and a `tool-guide`
- Create wiki-links liberally, even to pages that don't exist yet (sets future research targets)
- Keep index files lightweight — they exist for navigation, not content
- Rating system (1-7, Kepano-style) for how essential each concept is to the learning goal

### Skill 4: `tutor`

**Purpose:** Interactive teaching from the knowledge base. Explains concepts, answers questions, generates exercises — all grounded in wiki content, not general LLM knowledge.

**Modes:**
- **Explain**: Walk through a concept from the wiki, adapted to the learner's level
- **Quiz**: Generate questions based on wiki content to test understanding
- **Drill**: Create practical exercises (e.g., "open FL Studio, set up a sidechain on your kick and bass using Fruity Limiter, here's exactly how...")
- **Clarify**: Answer specific questions by referencing relevant wiki pages
- **Connect**: Show how a concept relates to other things in the knowledge base

**Critical rules:**
- ONLY teach from the wiki content. If the question isn't covered, say so and offer to queue a research task
- Always reference which wiki page(s) the information comes from
- Calibrate to the learner's stated skill level (from `learner-profile.md`)
- For practical skills, give equipment-specific instructions (don't say "use an audio interface," say "on your Volt 476, do X")
- Socratic questioning to check understanding, not lecturing
- If the learner seems to already know something, skip ahead — don't waste their time

### Skill 5: `learning-profile`

**Purpose:** Maintains persistent state about the learner — what they know, what they're working on, what they should study next.

**`learner-profile.md` schema:**
```yaml
---
name: Alex
learning_style:
  input_mode: verbal-stream          # how the user communicates (verbal-stream, structured, terse)
  conceptual_approach: big-picture-first  # big-picture-first | detail-first | example-first
  learning_mode: build-then-learn    # build-then-learn | study-then-apply | mixed
  analogy_preference: cross-domain   # cross-domain | within-domain | minimal
  overwhelm_sensitivity: high        # how carefully to chunk and sequence material
  momentum_style: burst              # burst (deep focus sessions) | steady (daily habit) | mixed

tutor_persona:
  name: "Jarvis"
  personality: direct-mentor
  voice: british-male                # Kokoro TTS voice ID (null for text-only)
  verbosity: concise
  celebrate_progress: true
  use_cross_domain_analogies: true

domains:
  - name: FL Studio / Music Production
    skill_level: beginner
    equipment: [Volt 476, AT2035, FL Key 37, FL Studio]
    goals: [live mixing, vocal recording, basic mastering]
    completed_topics: []
    current_focus: null
    queued_topics: []
  - name: Capture One Pro / Photography
    skill_level: beginner
    equipment: [Fujifilm X-T4]
    goals: [portrait editing, color grading, professional output]
    completed_topics: []
    current_focus: null
    queued_topics: []
  - name: Obsidian / Knowledge Management
    skill_level: intermediate
    goals: [Dataview mastery, automation, MIDI integration]
    completed_topics: [basic vault setup, YAML frontmatter, tags]
    current_focus: Dataview queries
    queued_topics: []
last_updated: 2026-04-05
---
```

**Capabilities:**
- Show current status across all domains
- Recommend next topic based on prerequisites and learning sequence
- Update skill level and completed topics after a tutoring session
- Suggest cross-domain connections ("the signal chain concept in audio applies to your data pipeline work too")

---

## 4. The Overnight Pipeline

### Concept

Using Claude Code's `/schedule` command, the user queues learning goals at the end of their day. Overnight, the agent runs the `research-and-ingest` skill followed by the `wiki-builder` skill autonomously. By morning, the AI vault has new structured content ready for review.

### Example workflow

```
Evening:
  User: "I want to learn about vocal mixing techniques for my home studio setup"
  Agent: Queued. Will research overnight using your equipment context (Volt 476, AT2035, FL Studio).

Overnight (autonomous):
  1. research-and-ingest searches for:
     - FL Studio vocal mixing tutorials (recent, high-view-count)
     - Volt 476 gain staging documentation
     - AT2035 frequency response and recommended EQ curves
     - Community-recommended vocal chain plugins (free/stock FL Studio)
     - Common home studio vocal problems and solutions
  2. Deposits 8-12 structured source files in raw/
  3. wiki-builder synthesizes into:
     - wiki/vocal-mixing/_index.md
     - wiki/vocal-mixing/signal-chain.md
     - wiki/vocal-mixing/eq-and-compression.md
     - wiki/vocal-mixing/common-problems.md
     - wiki/vocal-mixing/recommended-plugins.md

Morning:
  User opens Obsidian, browses the new wiki
  User drags "signal-chain.md" into personal vault (they've internalized it)
  User asks the tutor skill to explain the compression section in more depth
```

---

## 5. Test Personas

### Persona 1: Alex (Self — primary test case)

- **Age:** 22
- **Background:** CS/Math double major, entering Data Science master's. Intermediate coder, beginner in music production and photo editing.
- **Equipment:** Fujifilm X-T4, Volt 476, AT2035, FL Key 37, FL Studio, Capture One Pro, Dell XPS 9315
- **Emotional triggers:** Overwhelm from too many learning goals at once. Frustration when AI gives generic or hallucinated answers instead of what people actually do.
- **What success looks like:** Wakes up to a well-organized wiki on a topic. Quickly understands the practical landscape. Feels like the learning is manageable rather than overwhelming.
- **What failure looks like:** Agent dumps generic textbook explanations. Recommends obscure tools nobody uses. Doesn't account for his specific gear. Creates more organizational overhead than it saves.

### Persona 2: Priya — Graduate researcher

- **Age:** 26
- **Background:** Statistics PhD student. Textbook-strong but struggles applying methods to her actual messy dataset.
- **Equipment:** R Studio, Python/pandas, university HPC cluster
- **Emotional triggers:** Imposter syndrome when code doesn't work. Pressure from advisor.
- **What success looks like:** Agent finds practical examples of her specific statistical method applied to similar datasets. Bridges the theory-to-practice gap.
- **What failure looks like:** Agent re-explains theory she already knows. Gives code that doesn't account for her data's quirks.

### Persona 3: Marcus — Career changer

- **Age:** 34
- **Background:** Former accountant learning web development. Zero programming background. Enrolled in a bootcamp.
- **Equipment:** MacBook Air, VS Code, basic terminal familiarity
- **Emotional triggers:** Feels dumb when documentation assumes prior knowledge. Paralyzed by too many framework choices.
- **What success looks like:** Agent identifies the ONE stack that most bootcamp grads actually use and land jobs with. Explains without assuming jargon. Builds confidence.
- **What failure looks like:** Agent suggests five different frameworks without ranking them. Uses jargon. Recommends bleeding-edge tools when he needs stable, well-documented ones.

### Persona 4: Jordan — Experienced dev learning new domain

- **Age:** 28
- **Background:** 5 years as a backend engineer. Learning ML/data science for a career transition.
- **Equipment:** Linux workstation, familiar with Docker, Python expert
- **Emotional triggers:** Impatient with over-explanation. Wants to know "how this is different from what I already know."
- **What success looks like:** Agent maps ML concepts to software engineering analogies they already understand. Skips Python basics entirely. Focuses on the genuinely new conceptual territory.
- **What failure looks like:** Agent explains what a function is. Treats them like a beginner. Doesn't leverage their existing expertise.

---

## 6. Key Design Decisions to Make

These are questions I need to answer as I prototype. They don't have obvious right answers — the prototype will reveal which direction works better.

### Architecture questions

1. **Single vault vs. dual vault?** Should the AI vault be a separate Obsidian vault, or a folder within my existing vault? Separate vault = cleaner separation, but harder to cross-reference. Subfolder = easier linking, but risk of the agent accidentally touching personal notes.

2. **How granular should wiki pages be?** One page per concept? One page per technique? One page per tool? Too granular = hard to read. Too consolidated = hard to reference specific things.

3. **Should the agent maintain its own CLAUDE.md memory file in the AI vault?** This could store its understanding of my learning state across sessions, separate from the learner-profile skill. Karpathy's approach has Claude auto-maintain index files — should my agent auto-maintain its own context file too?

4. **What's the right Obsidian template set for agent-generated notes?** I need templates for: research-source, wiki-article, lesson, exercise, concept-map. How do these compose with Kepano's system?

### Interaction design questions

5. **How much autonomy in research?** Should the agent always confirm research subtasks before executing, or should it just go? More confirmation = more control but slower. Less confirmation = faster but might waste compute on wrong directions.

6. **How should the agent handle "I don't have enough sources on this"?** Stop and tell me? Make a best-effort synthesis with caveats? Queue for deeper research?

7. **Should the tutor skill ever fall back to general LLM knowledge?** Strict grounding (only teach from wiki) is safer but might be frustrating if the wiki is thin on a topic. Allowing fallback with clear labeling ("this is from my general knowledge, not from researched sources") might be more practical.

8. **How should the agent handle conflicting sources?** Present both sides? Pick the more authoritative one? Flag the conflict and let me decide?

### Scope questions for the class prototype

9. **Which domain should I prototype first?** Music production (FL Studio) is deeply personal and would be the most satisfying test. But coding/data science might be easier to demo to classmates who can relate. Photo editing (Capture One) is niche.

10. **How much of the overnight pipeline can I realistically demo?** Can I show a pre-built wiki as the "result" of an overnight run, even if I don't demo the actual scheduled execution?

11. **What's the minimum viable skill set for the in-class demo?** Probably session-router + tutor + a pre-built wiki. Research-and-ingest and wiki-builder are harder to demo live but essential to the concept.

### Voice & personality questions

12. **How deeply should persona affect the skill prompts?** Should every skill have persona-specific instructions, or should only the tutor skill change based on persona? More pervasive = more consistent character, but more complex to maintain.

13. **Should the agent have a name by default, or should naming it be part of the user setup?** A default name (like "Jarvis") gives it instant personality. Letting the user choose creates ownership. Could offer both — a default with easy rename.

14. **How to handle the voice layer failing or being unavailable?** The text experience needs to stand on its own. Voice is additive. But should the text output be written differently when it knows it'll be spoken aloud (shorter sentences, more conversational)?

15. **Where does "enjoyable to use" end and "anthropomorphized too much" begin?** The agent should feel like a helpful presence, not a friend or companion. It's a tool with personality, not a relationship.

---

## 7. Technical Stack

| Component | Tool | Notes |
|---|---|---|
| Agent framework | Claude Code Skills (.claude/skills/) | As required by class |
| LLM | Claude (via Claude Code) | For prototype; production could use Groq/Llama for cost |
| Search/retrieval | Claude Code web search | For prototype; Tavily for production agent |
| Knowledge base | Obsidian vault (markdown files) | Karpathy-style structure |
| Overnight automation | Claude Code `/schedule` | Queue research tasks |
| Version control | Git + GitHub | Required by class |
| Note structure | Kepano-style YAML + wiki-links | Categories, composable templates |
| TTS (voice output) | Kokoro TTS | Open source, local, multi-voice. Future feature. |
| STT (voice input) | Handy (Whisper/Parakeet) | System-wide dictation, 17k+ GitHub stars |
| Voice trigger | Bome MIDI Translator Pro + FL Key 37 | Existing infrastructure, pad-to-script routing |

---

## 8. What I Admire and Want to Incorporate

### From NotebookLM
- Grounded synthesis from actual documents
- Transparent sourcing — you can see what it's drawing from
- The "podcast" format — making dense material conversational and accessible

### From Karpathy's Obsidian RAG
- No vector database, no embeddings — just clever file structure
- `raw/` → `wiki/` pipeline with index files for navigation
- Claude Code as the query interface over markdown files
- Lightweight enough for a solo operator

### From Kepano's vault philosophy
- YAML frontmatter as schema (properties/categories)
- Wiki-links over folder hierarchy for organization
- Composable templates — a note can be multiple things
- Rating system (1-7) for importance
- "File over app" — the data outlasts any specific tool
- Speed and laziness as design goals

### From my own experience with AI tools
- **What people actually do > what could theoretically work.** Real community adoption matters.
- **Equipment-specific advice is 10x more useful** than generic advice
- **I don't need AI to teach me coding** — AI is already good at that interactively. I need it for domains where the knowledge is scattered and hard to synthesize (music production, photo editing, domain-specific workflows)

### From the Jarvis / AI companion concept
- A persistent, always-ready presence that knows your context and adapts to you
- Voice makes the interaction feel natural and allows hands-free learning while working
- Personality makes the difference between a tool you tolerate and a tool you want to use
- The AI desk pet trend proves people want this — they want their AI to feel like *theirs*, not generic
- But Jarvis works because it's competent first, personable second — personality without capability is a toy

---

## 9. Success Criteria

The agent prototype is successful if:

1. A classmate can interact with it and understand the value proposition within 2 minutes
2. The tutor skill teaches from the knowledge base, not from general knowledge — and this is visibly different from just asking Claude
3. The overnight pipeline concept is clear even if it's demoed with pre-built content
4. The source quality filtering is visible — the agent can explain why it chose certain sources over others
5. Personalization is visible — it references specific equipment and adjusts to stated skill level
6. I personally find the output useful for one of my actual learning goals
7. The tutor persona affects the interaction tone in a noticeable, consistent way — switching personas changes the experience
8. The agent handles messy, spoken-style input gracefully without asking the user to rephrase
9. Using the agent feels *enjoyable* — not like another chore. The personality, the low friction, the voice concept all serve this goal
10. The agent makes me feel like my learning is manageable rather than overwhelming — clear next steps, chunked material, progress markers

---

## 10. Risks and Potential Failure Modes

- **Over-engineering the knowledge base structure** instead of getting a working prototype fast
- **The wiki-builder creates low-quality summaries** that are worse than just reading the original sources
- **Source quality filtering is too strict** and the agent can't find enough material on niche topics
- **The overnight pipeline is cool in concept but impractical** — maybe I'd rather direct the research interactively
- **Scope creep** — trying to support all my learning domains in the prototype instead of focusing on one
- **The dual-vault architecture adds complexity** without enough benefit for a prototype — maybe start with a single vault section
- **Personality customization becomes a distraction** — spending time tweaking tutor personas instead of building core research/synthesis skills
- **Voice output is too slow or awkward** — TTS latency breaks the conversational flow and makes text feel preferable
- **The agent feels too "human" and creates false expectations** — users expect it to remember things or have continuity it doesn't actually have
- **Designing for my own learning style makes it too narrow** — what works for a verbal-processor-build-first learner might not transfer to the class demo personas

---

## 11. Open Ideas & Future Directions (Post-Prototype)

### Voice & interaction

- **Full Jarvis mode**: MIDI pad triggers Handy (STT) → agent processes → Kokoro (TTS) speaks response. Hands-free learning while working in FL Studio or Capture One.
- **Voice-guided walkthroughs**: Agent narrates step-by-step instructions while the user follows along in the application. "Okay, now open the mixer, find channel 3, and insert Fruity Parametric EQ 2."
- **Multiple tutor voices for different domains**: British mentor for music theory, enthusiastic peer for coding, patient coach for math. Different voices reinforce domain context-switching.
- **AI desk companion**: A small always-on widget or dedicated device (like the AI desk pets you see online) that shows the tutor persona's status, current learning streak, next topic, and responds to voice. Low priority but high "want to use this" factor.
- **NotebookLM-style audio lessons**: Agent generates a conversational podcast-format lesson from wiki content, rendered through Kokoro TTS. Listen during walks, commutes, or downtime. (Directly builds on the podcast agent project already in progress.)

### Knowledge & learning

- **Spaced repetition integration**: Agent generates Anki-style flashcards from wiki content, timed to reinforce learning
- **Practice drill generator**: Domain-specific exercises calibrated to skill level (e.g., "mix this reference track to match this target")
- **Cross-domain connection finder**: "The signal chain concept in audio is analogous to the data pipeline concept in engineering"
- **Learning velocity tracker**: How fast am I progressing in each domain? Where am I stalling?
- **Community source monitor**: Agent watches specific subreddits, forums, or YouTube channels for new content relevant to queued learning goals
- **Multi-agent version**: One agent researches, another synthesizes, another teaches — specialized agents with handoff protocols
- **Export to other formats**: Generate a lesson as a podcast script (NotebookLM-style), a slide deck, or a practical checklist
- **"Teach-back" mode**: Agent asks the user to explain a concept back to it, evaluates the explanation, and identifies gaps — one of the most effective learning techniques, now automated

---

*This document is a living design brief. Update it as the prototype reveals what works and what doesn't. The prototype is not the deliverable — the insights are.*
