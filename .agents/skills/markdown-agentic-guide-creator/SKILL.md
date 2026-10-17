---
name: markdown-agentic-guide-creator
description: Generate a machine-readable, unclipped Markdown (.md) specification containing architectural guidelines, gap analyses, and delimited code files for autonomous coding agents like Antigravity. Use when the user asks for markdown-agentic-guide-creator, markdown-gentic-guide-creator, or to package codebases, skills, or architectures into an unclipped agentic markdown guide while saving chat output tokens.
---
# markdown-agentic-guide-creator

Generate self-contained, machine-parseable Markdown (`.md`) specifications containing architectural gap analyses, reference guidelines, and delimited code files designed for direct ingestion by autonomous coding agents (such as Antigravity or Gemini CLI) while saving conversational output tokens.

## When to Use

- The user asks for `markdown-agentic-guide-creator`, `markdown-gentic-guide-creator`, or requests packaging code, guidelines, or skill upgrades into a single `.md` guide file.
- The user wants to pass a single specification file to an AI coding agent to scaffold, refactor, or patch a project without streaming hundreds of lines into the chat window.
- The user requests "generate an agentic markdown guide" or "save the whole architecture as an ingestion guide".
- An existing codebase or multi-file system needs a clean, unpackable bundle that another agent can parse and execute deterministically.

## Steps

### 1. Analyze Input and Design Modular Architecture

Inspect the user's requirements, source repository, or problem brief. Structure the target solution into a modular file tree:

- **Architecture Overview**: Executive context, design trade-offs, and dependency map.
- **Dispatch / Routing Table**: Quick lookup linking functional requirements to target files.
- **Modular Code Blocks**: The complete, production-ready code for every required file, without ellipsis (`...`) or placeholder comments.
- **Agent Ingestion Command**: Exact instructions and command-line scripts to unpack the files.

### 2. Format Delimited File Blocks for Machine Parsing

To allow downstream coding agents or automated unpacker scripts to extract files without ambiguity:

- Wrap every file in explicit start and end boundary markers:
  ```text
  === BEGIN FILE: <relative/path/to/file> (<language>) ===
  ```
  and
  ```text
  === END FILE: <relative/path/to/file> ===
  ```
- **Fencing Protection**: When the payload contains code or nested Markdown (which itself uses triple backticks ```), wrap the entire code block in **quadruple backticks (````)** to prevent early fence termination:
  ````markdown
  === BEGIN FILE: docs/example.md (markdown) ===
  ````markdown
  # Sub-document
  ```bash
  echo "Nested triple backticks remain intact"
  ```
  ````
  === END FILE: docs/example.md ===
  ````
- End the entire specification document with a strict sentinel marker:
  ```text
  === END OF SPECIFICATION ===
  ```

### 3. Write Directly to Disk (Zero Chat Token Leakage)

Never dump the entire generated Markdown specification into the chat response. Streaming large multi-file guides into chat exhausts output tokens and causes silent mid-file cutoffs.

- Use your environment's file-writing tool (`write_to_file`) or a deterministic Python script to persist the file directly to disk (e.g., in `docs/agent_specs/spec_<name>.md`).
- If scripting, use the bundled generator script `build_agent_spec_md.py` to assemble files deterministically.

### 4. Provide Ingestion Instructions for the Downstream Agent

Include a standardized **Agent Ingestion Section** at the bottom of the Markdown file:

```markdown
## Downstream Agent Ingestion Instructions

1. Parse every block demarcated by `=== BEGIN FILE: <path> (<lang>) ===` and `=== END FILE: <path> ===`.
2. Extract the inner code or content verbatim.
3. Create parent directories as needed and write each file to its designated relative path.
4. Verify file syntax and permissions (e.g., `chmod +x` for shell scripts).
5. Verify the terminating sentinel: `=== END OF SPECIFICATION ===`.
```

### 5. Verify Specification Completeness Before Responding

Verify that the file on disk is complete and untruncated before concluding the turn:

1. Read the last 500 bytes or final lines of the generated file.
2. Assert that `=== END OF SPECIFICATION ===` is present at the very end.
3. Check that all code fences are properly balanced and closed.

```python
with open(spec_file_path, "r", encoding="utf-8") as f:
    content = f.read()

assert "=== END OF SPECIFICATION ===" in content, "Error: Markdown specification was truncated!"
assert content.count("````") % 2 == 0, "Error: Unbalanced quadruple code fences detected!"
```

### 6. Minimal Chat Output Handoff

Once the file is written and verified:
- Provide a concise 3 to 5 bullet summary:
  - Destination path of the generated `.md` specification.
  - Total number of files and modules packaged inside.
  - High-level architecture summary.
  - One-line command for the next agent to unpack or ingest it.
- **Do NOT** duplicate the markdown file's internal code blocks in the chat response.

## Gotchas

- **Fence Collisions**: Standard markdown renderers break if an inner code block uses triple backticks and the outer container also uses triple backticks. Always use quadruple backticks ```` for the outer file container, or rely on explicit `=== BEGIN FILE ===` text markers.
- **Incomplete Placeholders**: Never allow the agent to write `# ... rest of code goes here ...` inside a specification file. Every file block must be 100% complete and drop-in ready.
- **Directory Traversal**: When designing unpackers, sanitize relative paths to prevent directory traversal outside the target workspace (e.g., disallow `../../`).
- **Token Inflation**: Printing the generated markdown in chat defeats the purpose of the skill. Always write to disk and return only metadata.
