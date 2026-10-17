#!/usr/bin/env python3
"""
unpack_agent_spec.py
Deterministically unpacks files from an agentic Markdown specification document.
Part of the markdown-agentic-guide-creator skill.
"""

import os
import re
import sys
import argparse


def unpack_spec(spec_file: str, target_dir: str = ".") -> int:
    """
    Parses a specification Markdown file and extracts all files enclosed in
    === BEGIN FILE: <path> (<lang>) === ... === END FILE: <path> === delimiters.
    """
    if not os.path.exists(spec_file):
        print(f"Error: Specification file not found: {spec_file}", file=sys.stderr)
        return 1

    with open(spec_file, "r", encoding="utf-8") as f:
        content = f.read()

    # Verify sentinel
    if "=== END OF SPECIFICATION ===" not in content:
        print("Warning: Missing '=== END OF SPECIFICATION ===' sentinel! File may be truncated.", file=sys.stderr)

    # Regex to capture file delimiters and content
    # Matches: === BEGIN FILE: <path> (<lang>) === \n(````[lang]\n)?(content)\n(````)?\n=== END FILE: <path> ===
    pattern = re.compile(
        r"=== BEGIN FILE:\s*([^\s()]+)(?:\s*\([^)]*\))?\s*===\s*\n"
        r"(?:````[a-zA-Z0-9_-]*\s*\n)?"
        r"(.*?)\n"
        r"(?:````\s*\n)?"
        r"=== END FILE:\s*\1\s*===",
        re.DOTALL
    )

    matches = list(pattern.finditer(content))
    if not matches:
        # Fallback simpler delimiter pattern
        simple_pattern = re.compile(
            r"=== BEGIN FILE:\s*([^\s()]+).*?===\s*\n(.*?)\n=== END FILE:\s*\1\s*===",
            re.DOTALL
        )
        matches = list(simple_pattern.finditer(content))

    if not matches:
        print("No delimited files found matching '=== BEGIN FILE: <path> ==='", file=sys.stderr)
        return 1

    extracted_count = 0
    for match in matches:
        rel_path = match.group(1).strip()
        body = match.group(2)

        # Strip surrounding 4-backtick or 3-backtick fence if present
        body = re.sub(r"^````[a-zA-Z0-9_-]*\n", "", body)
        body = re.sub(r"\n````$", "", body)

        # Security check: prevent directory traversal
        norm_path = os.path.normpath(rel_path)
        if norm_path.startswith("..") or os.path.isabs(norm_path):
            print(f"Skipping dangerous path: {rel_path}", file=sys.stderr)
            continue

        dest_full = os.path.join(target_dir, norm_path)
        os.makedirs(os.path.dirname(dest_full), exist_ok=True)

        with open(dest_full, "w", encoding="utf-8") as out:
            out.write(body + "\n")

        print(f"Extracted: {norm_path} ({len(body.encode('utf-8')):,} bytes)")
        extracted_count += 1

    print(f"\nSuccessfully unpacked {extracted_count} file(s) into '{target_dir}'.")
    return 0


def main():
    parser = argparse.ArgumentParser(
        description="Unpack files from an agentic Markdown specification."
    )
    parser.add_argument("spec_file", help="Path to the specification .md file")
    parser.add_argument(
        "--target-dir", "-t", default=".", help="Target directory for extracted files (default: .)"
    )

    args = parser.parse_args()
    sys.exit(unpack_spec(args.spec_file, args.target_dir))


if __name__ == "__main__":
    main()
