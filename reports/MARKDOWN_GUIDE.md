# Team Markdown Guide
Our team uses **Markdown (.md)** for all reports and documentation. Markdown is a lightweight markup language that converts plain text into formatted content.

## Why Markdown?
1.  **Version Control:** It is plain text, so `git diff` works perfectly to show changes.
2.  **Readability:** It is readable as raw code AND as rendered HTML.
3.  **Standard:** It is the standard for GitHub documentation (READMEs).

## Basic Syntax Cheat Sheet

### 1. Headers
Use `#` for headers. The number of hashtags indicates the hierarchy.
# H1 (Main Title - Use once per doc)
## H2 (Major Section)
### H3 (Subsection)

### 2. Lists
**Bullet Points:** Use asterisks `*` or hyphens `-`.
* Item A
* Item B
  * Nested Item (indent with 2 spaces)

**Numbered Lists:** Use numbers followed by a period `1.`.
1. First Step
2. Second Step

### 3. Text Formatting
* **Bold:** Wrap text in double asterisks: `**This is bold**` → **This is bold**
* *Italic:* Wrap text in single asterisks: `*This is italic*` → *This is italic*
* `Code`: Wrap short code or filenames in backticks: `` `filename.md` `` → `filename.md`

### 4. Code Blocks
For longer code snippets or terminal commands, use triple backticks.
```python
def hello():
    print("This is a code block")
