---
name: pdf-agentic-guide-creator
description: Generate a machine-readable, unclipped PDF specification containing markdown guidelines, architecture tables, and delimited code files for coding agents like Antigravity. Use when the user asks to analyze a codebase, skill, or workflow and output only a PDF guide or specification for agentic ingestion while saving chat output tokens.
---
# pdf-agentic-guide-creator

Generate self-contained, machine-parseable PDF specifications containing architectural gap analyses, markdown reference guides, and executable scripts designed for direct ingestion by autonomous coding agents (such as Antigravity) while keeping chat responses minimal to save output tokens.

## When to Use

- The user references `pdf-agentic-guide-creator` or asks to package code, guidelines, or skill upgrades into a machine-readable PDF.
- The user wants to pass a single specification document to an AI coding agent (e.g., Antigravity) to create, patch, or upgrade a repository or skill.
- The user requests "only return a PDF" to conserve chat output tokens instead of printing long markdown and code blocks in the conversation.
- An existing skill, archive, or tool needs a structured gap analysis paired with ready-to-extract modular files and scripts.

## Steps

### 1. Analyze Input and Design the Modular Architecture

Inspect the user's uploaded files, skill archives, or requirements to identify architectural gaps and required modules. Organize the proposed solution into a clean file tree separating:

- **Master Router / Entrypoint**: Updates or patches to the primary entry file (e.g., `SKILL.md` or `README.md`) with a dispatch table mapping triggers to modules.
- **Modular Reference Guides**: Focused markdown files (`references/*.md`) covering specific rules, workflows, and remediation heuristics.
- **Executable Scripts**: Standalone scripts (`scripts/*`) that automate verification, auditing, or execution.

### 2. Format Content for Machine Readability

Structure all file blocks inside the PDF so an automated agent or parser can extract them deterministically without ambiguity:

- Wrap every file or patch block in explicit start and end markers: `=== BEGIN FILE: <relative/path/to/file> (<language>) ===` and `=== END FILE: <relative/path/to/file> ===`.
- Keep the inner text of `Preformatted` code blocks pure so line-by-line extraction yields valid syntax without extra wrapper noise.
- Include a dedicated **Agent Ingestion Prompt** section at the end of the PDF instructing the target agent (e.g., Antigravity) on how to parse the delimiters, write the files, set permissions (`chmod +x`), and validate syntax.
- End the document with a sentinel marker: `=== END OF SPECIFICATION ===`.

### 3. Build an Unclipped PDF via Python ReportLab

Use `google:ds_python_interpreter` with `reportlab.platypus` (`SimpleDocTemplate`, `Paragraph`, `Preformatted`, `Table`, `Spacer`) rather than fixed-height HTML canvas containers that can clip overflowing code blocks at page boundaries.

Follow these layout and wrapping rules in Python:

1. **Wrap Long Code Lines**: Before passing code or markdown strings into `Preformatted`, wrap lines at 90 to 92 characters using `textwrap.wrap(..., break_long_words=True, break_on_hyphens=False)` while preserving leading indentation so no horizontal clipping occurs.
2. **Use Splittable Flowables**: Place each file header (`Paragraph`), wrapped code body (`Preformatted`), and file footer (`Paragraph`) directly into the `story` list so ReportLab splits long files cleanly across pages.
3. **High-Contrast Monospace Styling**: Use `Courier` at `7.5pt` to `8pt` with `10pt` leading on a light slate background (`#F8FAFC`) with a subtle border (`#CBD5E1`) for maximum OCR and PDF text-extractor accuracy.

```python
import textwrap

def wrap_code(text, width=92):
    lines = []
    for line in text.strip('\n').split('\n'):
        if len(line) <= width:
            lines.append(line)
        else:
            indent = len(line) - len(line.lstrip(' '))
            sub_indent = ' ' * min(indent + 2, 16)
            wrapped = textwrap.wrap(
                line,
                width=width,
                subsequent_indent=sub_indent,
                break_long_words=True,
                break_on_hyphens=False
            )
            lines.extend(wrapped)
    return '\n'.join(lines)
```

### 4. Verify PDF Completeness Before Responding

Never return a PDF without verifying that the final block rendered completely. In the same Python execution script after `doc.build(story)`:

1. Open the generated PDF with `pypdf.PdfReader`.
2. Extract the text of the final page (`reader.pages[-1].extract_text()`).
3. Assert that the sentinel string `=== END OF SPECIFICATION ===` is present on the last page and print the total page count.

```python
from pypdf import PdfReader

reader = PdfReader(pdf_filename)
last_page_text = reader.pages[-1].extract_text()
assert "=== END OF SPECIFICATION ===" in last_page_text, "PDF was truncated before the end marker!"
```

### 5. Minimize Chat Output to Save Tokens

Once the PDF is generated and verified:

- Start the response with the mandatory file confirmation and `[file-tag: code-generated-file-...]` tag.
- Provide only a brief 3 to 5 bullet summary of the sections included in the PDF.
- Do not print or repeat the markdown files, code scripts, or ingestion prompts in the chat text response. All detailed code and guidelines must live exclusively inside the PDF.

## Gotchas

- **Page-Boundary Truncation**: HTML-to-PDF engines and `KeepTogether` wrappers often clip code blocks that exceed a single page height. Always append `Preformatted` blocks directly to the ReportLab `story` list without wrapping large files in `KeepTogether`.
- **Special Character Corruption in Code**: Standard PDF fonts (`Helvetica`, `Courier`) only support Latin-1 characters. Replace Unicode box-drawing characters or emojis inside code blocks with standard ASCII equivalents (`+--`, `|--`, `->`, `[OK]`) so characters do not render as black squares.
- **Token Leakage in Chat**: Printing the full code in the chat response before or after generating the PDF defeats the token-saving purpose of this workflow. Keep the chat response strictly to the file link and high-level table of contents.