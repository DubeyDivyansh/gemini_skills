<div align="center">

<img src="assets/hero.svg" alt="gemini_skills - Autonomous AI Agent Skills" width="100%" />

<p align="center">
  <a href="https://github.com/DubeyDivyansh/gemini_skills/stargazers"><img src="https://img.shields.io/github/stars/DubeyDivyansh/gemini_skills?style=flat-square&color=38BDF8" alt="GitHub Stars" /></a>
  <a href="https://github.com/DubeyDivyansh/gemini_skills/network/members"><img src="https://img.shields.io/github/forks/DubeyDivyansh/gemini_skills?style=flat-square&color=818CF8" alt="GitHub Forks" /></a>
  <a href="https://github.com/DubeyDivyansh/gemini_skills/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-MIT-34D399?style=flat-square" alt="MIT License" /></a>
  <a href="https://github.com/DubeyDivyansh/gemini_skills/issues"><img src="https://img.shields.io/github/issues/DubeyDivyansh/gemini_skills?style=flat-square&color=F59E0B" alt="Open Issues" /></a>
  <img src="https://img.shields.io/badge/Status-Production--Ready-10B981?style=flat-square" alt="Production Ready" />
</p>

---

</div>

## Overview

**`gemini_skills`** is an open, production-grade skills catalog for autonomous AI agents, including **Google Antigravity**, **Gemini CLI**, **Claude Code**, and agentic coding platforms. 

Rather than letting LLMs generate sprawling, token-draining chat outputs or chaotic tabular blobs, `gemini_skills` provides deterministic SOPs, structured schema contracts, and Python execution tools that enforce:

1. **Massive Token Conservation** — Encapsulate deep codebase specifications and multi-file packages into unclipped, machine-parseable PDFs and Markdown files instead of leaking thousands of tokens into chat context.
2. **High-Signal Information Architecture** — Convert messy transcripts, technical specs, and meeting notes into standardized Markdown matrices built on proven archetype templates.

---

## Architecture & Execution Flow

<div align="center">
  <img src="assets/architecture.svg" alt="Autonomous Skill Discovery & Execution Cycle" width="100%" />
</div>

```
User Prompt ──> Skill Trigger Match ──> Deterministic SOP ──> Verified Output
```

---

## Included Skills

### 1. `pdf-agentic-guide-creator`

> **Save up to 85% of chat output tokens when transferring deep architectures, skills, or codebase updates between agents.**

- **Primary Goal:** Generates self-contained, machine-parseable PDF specifications containing architectural gap analyses, markdown reference guides, and executable code files designed for direct ingestion by coding agents.
- **Why It Matters:** Printing multiple files and long code blocks in chat exhausts conversation token limits and causes truncation. This skill directs the agent to generate an unclipped ReportLab Platypus PDF with explicit boundary markers and return only a compact summary and file handle.
- **Core Mechanism:**
  - Wraps files in explicit delimiters: `=== BEGIN FILE: <path> (<lang>) ===` and `=== END FILE: <path> ===`.
  - Enforces text wrapping at 90–92 characters to eliminate horizontal clipping in monospace flowables.
  - Generates splittable flowables via `reportlab.platypus` across page boundaries (no `KeepTogether` page clipping).
  - Verifies document integrity with sentinel assertion: `assert "=== END OF SPECIFICATION ===" in last_page`.
- **Reference Script:** Included at [`skills/pdf-agentic-guide-creator/scripts/build_agent_spec_pdf.py`](skills/pdf-agentic-guide-creator/scripts/build_agent_spec_pdf.py).

---

### 2. `markdown-agentic-guide-creator`

> **Generate machine-readable, unclipped Markdown (`.md`) specifications with deterministic unpacking CLI tooling.**

- **Primary Goal:** Package multi-file architectures, gap analyses, and executable code into a single unclipped `.md` specification file designed for zero-chat-token leakage and automated agent ingestion.
- **Why It Matters:** Downstream agents frequently choke when extracting code blocks from markdown due to unclosed fences, nested triple-backtick collisions, or truncated conversational outputs. This skill provides explicit fencing rules and companion Python scripts to build and unpack specifications automatically.
- **Core Mechanism:**
  - **Quadruple-Backtick Protection:** Wraps code blocks in ```` ```` fences so inner markdown documents (containing standard triple backticks) do not prematurely terminate the file block.
  - **Explicit Boundaries:** Uses `=== BEGIN FILE: <path> (<lang>) ===` and `=== END FILE: <path> ===` for regex-safe parsing.
  - **Automated Round-Trip Tooling:**
    - [`build_agent_spec_md.py`](skills/markdown-agentic-guide-creator/scripts/build_agent_spec_md.py): Deterministically packages directories and files into a validated `.md` specification.
    - [`unpack_agent_spec.py`](skills/markdown-agentic-guide-creator/scripts/unpack_agent_spec.py): Parses any specification and safely unpacks all files to target directories (with path traversal guards).
  - **Sentinel Gate:** Ensures zero-truncation with `=== END OF SPECIFICATION ===`.
- **Sample Specification:** See [`skills/markdown-agentic-guide-creator/examples/sample_agent_spec.md`](skills/markdown-agentic-guide-creator/examples/sample_agent_spec.md).

#### Benchmark Comparison: Chat Dump vs. Agentic Spec Packages

| Metric | Raw Chat Dumps | `pdf-agentic-guide-creator` | `markdown-agentic-guide-creator` |
| :--- | :--- | :--- | :--- |
| **Output Token Footprint** | 4,000 – 12,000+ tokens | < 150 tokens in chat | < 150 tokens in chat |
| **Parsing Determinism** | Low (backtick escaping errors) | High (delimited PDF) | 100% via bundled `unpack_agent_spec.py` |
| **Fence Collision Safety** | Frequent syntax errors | N/A (Flowable PDF) | Protected via quadruple backticks (````) |
| **Human Readability** | Disorganized in long threads | Clean multi-page document | Native GitHub Flavored Markdown |
| **Automated Verification** | None | Sentinel check on last page | Sentinel check + unclosed fence assertion |

---

### 3. `table-summarizer`

> **Instantly transform unstructured text, transcripts, and messy data dumps into high-signal Markdown matrices.**

- **Primary Goal:** Summarize unstructured text, articles, meetings, data, or documents into structured Markdown tables tailored to the subject archetype.
- **Why It Matters:** Unstructured notes and walls of text slow down human decision-making and agent parsing. `table-summarizer` categorizes the input into one of five proven archetypes and enforces strict density and scannability standards.
- **The 5 Archetypes:**
  1. **Action Items & Meetings** (`Topic`, `Decision / Task`, `Owner`, `Due Date / Status`)
  2. **Comparative Analysis** (`Feature / Dimension`, `Option A`, `Option B`, `Recommendation / Notes`)
  3. **Executive / Research Synthesis** (`Key Finding`, `Evidence / Details`, `Impact / Significance`)
  4. **Chronological / Milestone Tracking** (`Phase / Date`, `Milestone`, `Deliverables`, `Status`)
  5. **Pros & Cons / Trade-offs** (`Category`, `Advantage`, `Disadvantage`, `Mitigation`)
- **Key Rules:**
  - Always lead with a 1–2 sentence executive overview.
  - Zero vague headers (`Info` or `Details` are strictly forbidden; use `Mechanism`, `Impact`, `Action Item`).
  - Bold key numbers, verdicts, and entity names for rapid scannability.
  - Accompany with 2–3 concise synthesis bullet points directly below the table.
- **Detailed Reference:** See [`skills/table-summarizer/examples/archetypes_guide.md`](skills/table-summarizer/examples/archetypes_guide.md).

---

## Directory Layout

```
gemini_skills/
├── assets/
│   ├── hero.svg                            # Project-native pure SVG hero banner
│   └── architecture.svg                    # Visual agent workflow diagram
├── skills/
│   ├── markdown-agentic-guide-creator/     # NEW: Markdown agentic spec generator & unpacker
│   │   ├── SKILL.md                        # Operational instructions & trigger rules
│   │   ├── scripts/
│   │   │   ├── build_agent_spec_md.py      # Packages files into unclipped spec.md
│   │   │   └── unpack_agent_spec.py        # Extracts files from spec.md safely
│   │   └── examples/
│   │       └── sample_agent_spec.md        # Reference specification template
│   ├── pdf-agentic-guide-creator/
│   │   ├── SKILL.md                        # Operational instructions & trigger rules
│   │   └── scripts/
│   │       └── build_agent_spec_pdf.py     # Standalone ReportLab PDF generator script
│   └── table-summarizer/
│       ├── SKILL.md                        # Operational instructions & trigger rules
│       └── examples/
│           └── archetypes_guide.md         # Archetype patterns & reference templates
├── .agents/skills/                         # Direct link / compatibility mirror for agent runtimes
│   ├── markdown-agentic-guide-creator/
│   │   └── SKILL.md
│   ├── pdf-agentic-guide-creator/
│   │   └── SKILL.md
│   └── table-summarizer/
│       └── SKILL.md
├── .github/
│   └── workflows/
│       └── validate-skills.yml             # Automated syntax and frontmatter validator
├── tests/
│   └── test_skills.py                      # Automated test suite
├── CONTRIBUTING.md
├── LICENSE
└── README.md
```

---

## Quickstart & Installation

### Option 1: Integrate into Antigravity or Gemini CLI Projects

Simply clone or copy the desired skill folder directly into your workspace's `.agents/skills/` directory:

```bash
# Clone the repository
git clone https://github.com/DubeyDivyansh/gemini_skills.git

# Copy skills to your project's agent skills directory
cp -r gemini_skills/skills/* /path/to/your/workspace/.agents/skills/
```

### Option 2: Build & Unpack Markdown Specifications

```bash
# Package files into a specification markdown document
python skills/markdown-agentic-guide-creator/scripts/build_agent_spec_md.py \
  --output agent_spec.md \
  --title "Microservice Architecture Package" \
  --summary "Full specification and source code for downstream agent ingestion." \
  --file "src/main.py" "./local_main.py" \
  --file "config.json" "./local_config.json"

# Unpack the specification into a target directory
python skills/markdown-agentic-guide-creator/scripts/unpack_agent_spec.py agent_spec.md --target-dir ./out
```

### Option 3: Run the Spec PDF Generator Standalone

```bash
pip install reportlab pypdf

# Generate unclipped agent specification PDF
python skills/pdf-agentic-guide-creator/scripts/build_agent_spec_pdf.py \
  --output agent_spec.pdf \
  --title "Core Auth Module Refactor" \
  --summary "Gap analysis and modular code package for token-safe ingestion." \
  --file "src/auth.py" "./local_auth.py"
```

---

## Quality & Design Principles

All skills in this repository follow strict operational standards:

* **Surgical & Deterministic:** Skills focus on deterministic Python code and strict SOP boundaries rather than probabilistic LLM guesswork.
* **Compatibility First:** Fully compatible with Antigravity 2.0, Gemini CLI, Claude Code, and Cursor agent environments.
* **Self-Contained:** Each skill contains its own triggers, execution rules, edge-case remediation, and verified gotchas.

---

## Contributing

Contributions of new agent skills, prompts, and deterministic execution tools are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on skill structure, frontmatter schemas, and testing.

---

## License

This repository is distributed under the [MIT License](LICENSE).
