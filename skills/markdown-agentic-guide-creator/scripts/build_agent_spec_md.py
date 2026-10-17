#!/usr/bin/env python3
"""
build_agent_spec_md.py
Packages multiple source files into a single, unclipped, machine-parseable
Markdown specification document designed for autonomous AI coding agents.
Part of the markdown-agentic-guide-creator skill.
"""

import os
import sys
import argparse
from typing import List, Dict, Optional


def create_agent_spec_md(
    output_md_path: str,
    title: str,
    summary: str,
    files: List[Dict[str, str]],
    ingestion_prompt: Optional[str] = None,
) -> str:
    """
    Build a structured Markdown specification with delimited files and sentinel validation.

    :param output_md_path: Destination path for the generated markdown file.
    :param title: Title of the specification.
    :param summary: High-level overview and architectural summary.
    :param files: List of dicts: [{"path": "relative/path.ext", "lang": "python", "content": "..."}]
    :param ingestion_prompt: Optional explicit instructions for downstream agents.
    """
    lines = []

    # Title & Metadata
    lines.append(f"# SPECIFICATION: {title}\n")
    lines.append(f"> **Agent Ingestion Specification Package**  ")
    lines.append(f"> Auto-generated for autonomous coding agents (Antigravity, Gemini CLI, Claude Code).\n")
    lines.append(f"## Executive Architecture Summary\n")
    lines.append(f"{summary.strip()}\n")

    # Table of Contents
    lines.append(f"## Packaged Files Index\n")
    lines.append("| Index | Target File Path | Language | Size (bytes) |")
    lines.append("| :---: | :--- | :---: | :---: |")
    for idx, item in enumerate(files, 1):
        rel_path = item.get("path", f"file_{idx}")
        lang = item.get("lang", "text")
        size = len(item.get("content", "").encode("utf-8"))
        lines.append(f"| {idx} | `{rel_path}` | `{lang}` | {size:,} |")
    lines.append("\n---\n")

    # Delimited File Blocks
    lines.append(f"## Delimited Source Modules\n")
    for item in files:
        rel_path = item.get("path", "unknown")
        lang = item.get("lang", "text")
        content = item.get("content", "").strip("\n")

        lines.append(f"=== BEGIN FILE: {rel_path} ({lang}) ===")
        # Use quadruple backticks so embedded triple backticks don't terminate the block
        lines.append(f"````{lang}")
        lines.append(content)
        lines.append(f"````")
        lines.append(f"=== END FILE: {rel_path} ===\n")

    # Ingestion Instructions
    lines.append("## Downstream Agent Ingestion Instructions\n")
    if ingestion_prompt:
        lines.append(f"{ingestion_prompt.strip()}\n")
    else:
        lines.append("1. Parse all blocks bounded by `=== BEGIN FILE: <path> (<lang>) ===` and `=== END FILE: <path> ===`.")
        lines.append("2. Extract the inner content verbatim (stripping the enclosing 4-backtick fence).")
        lines.append("3. Create destination folders and write each file to its exact relative path.")
        lines.append("4. Confirm the sentinel termination marker below before proceeding with execution.\n")

    # Sentinel Marker
    lines.append("=== END OF SPECIFICATION ===")

    full_text = "\n".join(lines) + "\n"

    # Ensure parent directory exists
    parent_dir = os.path.dirname(output_md_path)
    if parent_dir:
        os.makedirs(parent_dir, exist_ok=True)

    with open(output_md_path, "w", encoding="utf-8") as f:
        f.write(full_text)

    # Verification
    with open(output_md_path, "r", encoding="utf-8") as f:
        verified = f.read()

    assert "=== END OF SPECIFICATION ===" in verified, "Verification failed: Sentinel missing!"
    print(f"Verified: '{output_md_path}' successfully built with {len(files)} packaged file(s).")
    return output_md_path


def main():
    parser = argparse.ArgumentParser(
        description="Build an unclipped, machine-parseable Markdown specification for AI coding agents."
    )
    parser.add_argument("--output", "-o", default="agent_specification.md", help="Output Markdown file path")
    parser.add_argument("--title", "-t", default="System Architecture Specification", help="Specification title")
    parser.add_argument("--summary", "-s", default="Machine-readable specification package.", help="Summary")
    parser.add_argument(
        "--file", "-f", action="append", nargs=2, metavar=("TARGET_PATH", "LOCAL_FILE"),
        help="Map relative target path to local content file (can be repeated)"
    )

    args = parser.parse_args()

    files_payload = []
    if args.file:
        for target_path, local_path in args.file:
            if os.path.exists(local_path):
                with open(local_path, "r", encoding="utf-8", errors="replace") as f:
                    ext = os.path.splitext(target_path)[1].lstrip(".") or "text"
                    files_payload.append({"path": target_path, "lang": ext, "content": f.read()})
            else:
                print(f"Warning: Local file not found: {local_path}", file=sys.stderr)

    create_agent_spec_md(
        output_md_path=args.output,
        title=args.title,
        summary=args.summary,
        files=files_payload,
    )


if __name__ == "__main__":
    main()
