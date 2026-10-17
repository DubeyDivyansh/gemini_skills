---
name: table-summarizer
description: Summarize unstructured text, articles, meetings, data, or documents into structured Markdown tables. Use when the user asks to summarize in a table, create a tabular summary, tabulate key points, convert notes or reports into a table format, or extract structured comparisons.
---
# Table Summarizer

Summarizes input content and organizes the information into high-signal, properly structured Markdown tables tailored to the subject matter.

## When to Use

* The user asks to "summarize in a table", "tabulate this", "create a table summary", or "put this in a table".

* The user provides long-form text, transcripts, articles, research papers, or documentation and asks for structured extraction.

* The user requests a comparison between entities, options, or strategies in a structured matrix.

## Workflow

1. Identify Content Archetype
   Determine the underlying format of the content and select appropriate table columns:
   * Action items and meetings: Topic, Decision / Task, Owner, Due Date / Status.
   * Comparative analysis: Feature / Dimension, Option A, Option B, Recommendation / Notes.
   * Executive / research synthesis: Key Finding, Evidence / Details, Impact / Significance.
   * Chronological / milestone tracking: Phase / Date, Milestone, Deliverables, Status.
   * Pros and cons / trade-offs: Category, Advantage, Disadvantage, Mitigation.

2. Lead with a Concise Overview
   Provide a 1 to 2 sentence executive context before displaying the table so the user understands the core takeaway immediately.

3. Build the Markdown Table
   * Use precise, descriptive column headers.
   * Ensure standard Markdown table syntax with clean alignment and divider rows.
   * Keep cell entries compact. Use concise phrases, metrics, or short bullet points rather than multi-sentence paragraphs.
   * Highlight key names, numbers, or verdicts using bold text for scannability.

4. Provide Synthesis
   Directly below the table, add 2 to 3 concise bullet points highlighting critical takeaways, risks, or immediate next actions if relevant.

## Gotchas

* Avoid bloated cells. If an explanation requires more than two sentences, break it into distinct columns or move elaboration to notes below the table.

* Never use generic headers like "Info" or "Details" when specific labels like "Mechanism", "Impact", or "Action Item" are possible.

* Maintain consistency across rows. Do not mix full sentences in one row with single-word fragments in another.
