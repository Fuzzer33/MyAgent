---
created: 2026-04-06
categories: [[category]]
tags: [obsidian, zettelkasten, dataview]
---

# Knowledge Management

```dataview
TABLE difficulty, rating, type
FROM ""
WHERE contains(file.frontmatter.categories, this.file.link)
SORT rating DESC
```
