---
created: 2026-04-09
categories: [[reference]]
type: plugin
tags: [obsidian, RAG, semantic-search, AI]
url: https://github.com/brianpetro/obsidian-smart-connections
rating: 7
---

# Smart Connections

Obsidian plugin (100K+ users) that enables semantic search across your vault using local embeddings. Ask questions in natural language, get answers grounded in YOUR notes.

## How It Works

1. Embeds all vault notes locally using HyDE (Hypothetical Document Embeddings)
2. Semantic search finds relevant notes ranked by similarity
3. Shows exactly what context goes to the model before sending
4. Local-first — no API key required for embeddings

## Installation

1. Obsidian → Settings → Community plugins → Browse
2. Search "Smart Connections" → Install → Enable
3. Settings: Embedding provider = Local (default), Update frequency = On save
4. Recommended exclusions: `templates/`, `attachments/` (optional: `raw/`)

## Integration with Learning Agent

- **Tutor fallback**: When topic not fully in vault, Smart Connections finds related notes
- **Cross-domain queries**: "How does X relate to Y?" searches both concepts
- **/obsidian-emerge**: Uses semantic clustering to detect patterns in episodes
- **/obsidian-health**: Detects duplicate/orphaned notes via semantic similarity

## Sources
- [GitHub](https://github.com/brianpetro/obsidian-smart-connections)
- [Smart Connections App](https://smartconnections.app/)
