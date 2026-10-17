#!/usr/bin/env python3
"""
build_agent_spec_pdf.py
Deterministic ReportLab generator for machine-readable, unclipped agentic PDF specifications.
Part of the pdf-agentic-guide-creator skill.
"""

import os
import sys
import argparse
import textwrap
from typing import List, Dict, Optional

try:
    from reportlab.lib.pagesizes import letter
    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus import (
        SimpleDocTemplate,
        Paragraph,
        Preformatted,
        Spacer,
        Table,
        TableStyle,
        KeepTogether,
    )
except ImportError:
    print("Error: reportlab is required. Install via: pip install reportlab", file=sys.stderr)
    sys.exit(1)


def wrap_code(text: str, width: int = 92) -> str:
    """
    Wrap long code and markdown lines to avoid horizontal overflow in PDF preformatted flowables.
    Preserves leading whitespace indentation.
    """
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
                break_on_hyphens=False,
            )
            lines.extend(wrapped)
    return '\n'.join(lines)


def clean_ascii(text: str) -> str:
    """
    Replace non-Latin-1 characters and common unicode box glyphs with ASCII
    equivalents to prevent rendering black boxes in standard PDF Type 1 fonts.
    """
    replacements = {
        '—': '--',
        '–': '-',
        '“': '"',
        '”': '"',
        '‘': "'",
        '’': "'",
        '•': '*',
        '…': '...',
        '→': '->',
        '←': '<-',
        '│': '|',
        '─': '-',
        '┌': '+',
        '┐': '+',
        '└': '+',
        '┘': '+',
        '├': '+',
        '┤': '+',
        '┬': '+',
        '┴': '+',
        '┼': '+',
        '✓': '[OK]',
        '✔': '[OK]',
        '✗': '[X]',
        '✘': '[X]',
    }
    for orig, rep in replacements.items():
        text = text.replace(orig, rep)
    # Ensure standard latin-1 encoding safety
    return text.encode('latin-1', 'replace').decode('latin-1')


def create_agent_spec_pdf(
    output_pdf_path: str,
    title: str,
    summary: str,
    files: List[Dict[str, str]],
    ingestion_prompt: Optional[str] = None,
) -> str:
    """
    Build a multi-page, unclipped PDF specification suitable for autonomous agent ingestion.

    :param output_pdf_path: Path where the PDF will be saved.
    :param title: Specification Title.
    :param summary: High-level overview / gap analysis.
    :param files: List of dicts: [{"path": "relative/path.ext", "lang": "python", "content": "..."}]
    :param ingestion_prompt: Optional explicit prompt instructions for the agent parser.
    """
    doc = SimpleDocTemplate(
        output_pdf_path,
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=36,
        bottomMargin=36,
    )

    styles = getSampleStyleSheet()

    # Define custom styles
    title_style = ParagraphStyle(
        'SpecTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=colors.HexColor('#0F172A'),
        spaceAfter=8,
    )

    subtitle_style = ParagraphStyle(
        'SpecSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#475569'),
        spaceAfter=14,
    )

    file_header_style = ParagraphStyle(
        'FileHeader',
        parent=styles['Heading3'],
        fontName='Courier-Bold',
        fontSize=9,
        leading=12,
        textColor=colors.HexColor('#1E293B'),
        spaceBefore=10,
        spaceAfter=4,
    )

    code_style = ParagraphStyle(
        'MonospaceCode',
        parent=styles['Code'],
        fontName='Courier',
        fontSize=7.5,
        leading=10,
        textColor=colors.HexColor('#0F172A'),
        backColor=colors.HexColor('#F8FAFC'),
        borderColor=colors.HexColor('#CBD5E1'),
        borderWidth=0.5,
        borderPadding=6,
        spaceBefore=2,
        spaceAfter=6,
    )

    sentinel_style = ParagraphStyle(
        'Sentinel',
        parent=styles['Normal'],
        fontName='Courier-Bold',
        fontSize=9,
        leading=12,
        textColor=colors.HexColor('#059669'),
        alignment=1,  # Centered
        spaceBefore=16,
    )

    story = []

    # Title & Executive Summary
    story.append(Paragraph(clean_ascii(f"SPECIFICATION: {title}"), title_style))
    story.append(Paragraph(clean_ascii(summary), subtitle_style))
    story.append(Spacer(1, 10))

    # Architecture File Delimiters
    for item in files:
        rel_path = item.get('path', 'unknown')
        lang = item.get('lang', 'text')
        raw_content = item.get('content', '')

        # File header marker
        start_marker = f"=== BEGIN FILE: {rel_path} ({lang}) ==="
        story.append(Paragraph(clean_ascii(start_marker), file_header_style))

        # Formatted Code Body (Splittable across pages)
        wrapped_code_content = wrap_code(clean_ascii(raw_content), width=92)
        story.append(Preformatted(wrapped_code_content, code_style))

        # File end marker
        end_marker = f"=== END FILE: {rel_path} ==="
        story.append(Paragraph(clean_ascii(end_marker), file_header_style))
        story.append(Spacer(1, 8))

    # Optional Ingestion Prompt
    if ingestion_prompt:
        story.append(Paragraph("=== AGENT INGESTION INSTRUCTIONS ===", title_style))
        story.append(Paragraph(clean_ascii(ingestion_prompt), subtitle_style))
        story.append(Spacer(1, 10))

    # End of Specification Sentinel Marker
    story.append(Paragraph("=== END OF SPECIFICATION ===", sentinel_style))

    # Build the document
    doc.build(story)

    # Verification step
    try:
        from pypdf import PdfReader
        reader = PdfReader(output_pdf_path)
        last_page = reader.pages[-1].extract_text()
        assert "=== END OF SPECIFICATION ===" in last_page, "Verification failed: End sentinel missing!"
        print(f"Verified: '{output_pdf_path}' created successfully ({len(reader.pages)} pages).")
    except ImportError:
        print(f"Created: '{output_pdf_path}' (Install pypdf for automated end-to-end verification).")

    return output_pdf_path


def main():
    parser = argparse.ArgumentParser(
        description="Build an unclipped, machine-parseable PDF specification for AI coding agents."
    )
    parser.add_argument("--output", "-o", default="agent_specification.pdf", help="Output PDF file path")
    parser.add_argument("--title", "-t", default="System Specification", help="Specification title")
    parser.add_argument("--summary", "-s", default="Machine-readable specification package.", help="Summary")
    parser.add_argument(
        "--file", "-f", action="append", nargs=2, metavar=("PATH", "LOCAL_FILE"),
        help="Map relative target path to local content file (can be repeated)"
    )

    args = parser.parse_args()

    files_payload = []
    if args.file:
        for target_path, local_path in args.file:
            if os.path.exists(local_path):
                with open(local_path, "r", encoding="utf-8", errors="replace") as f:
                    ext = os.path.splitext(target_path)[1].lstrip('.') or "text"
                    files_payload.append({"path": target_path, "lang": ext, "content": f.read()})
            else:
                print(f"Warning: Local file not found: {local_path}", file=sys.stderr)

    create_agent_spec_pdf(
        output_pdf_path=args.output,
        title=args.title,
        summary=args.summary,
        files=files_payload,
    )


if __name__ == "__main__":
    main()
