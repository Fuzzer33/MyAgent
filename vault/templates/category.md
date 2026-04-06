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
