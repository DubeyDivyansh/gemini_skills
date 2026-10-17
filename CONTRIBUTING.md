# Contributing to gemini_skills

Thank you for your interest in contributing to `gemini_skills`! We welcome new agent skills, prompts, and deterministic execution tools.

## Skill Standards

Every skill submitted to this repository must meet the following criteria:

1. **Structured Frontmatter:**
   Must begin with valid YAML frontmatter:
   ```yaml
   ---
   name: your-skill-name
   description: Brief explanation of what the skill does and exact triggers for when to use it.
   ---
   ```

2. **Core Sections in `SKILL.md`:**
   - `# <skill-name>`: Title and 1-paragraph summary.
   - `## When to Use`: Explicit trigger conditions and negative triggers ("When NOT to use").
   - `## Workflow / Steps`: Step-by-step instructions for the agent.
   - `## Gotchas / Edge Cases`: Concrete solutions for known pitfalls.

3. **Deterministic Execution over LLM Guesswork:**
   - Push deterministic logic into Python scripts or templates (in `scripts/` or `examples/`).
   - Keep chat responses concise and token-efficient.

4. **Directory Structure:**
   ```
   skills/
   └── your-skill-name/
       ├── SKILL.md
       ├── scripts/       # Optional helper scripts
       ├── references/    # Optional reference markdown files
       └── examples/      # Optional example outputs
   ```

## Pull Request Process

1. Fork the repository.
2. Create your feature branch (`git checkout -b skill/new-skill-name`).
3. Commit your changes with clear messages (`git commit -m 'feat: add new-skill-name skill'`).
4. Push to your branch (`git push origin skill/new-skill-name`).
5. Open a Pull Request with a short summary and sample test run.
