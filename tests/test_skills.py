"""
test_skills.py
Validates SKILL.md frontmatter, schema, and structure.
"""

import glob
import os
import sys
import yaml


def test_skills():
    skill_files = glob.glob("skills/*/SKILL.md")
    assert len(skill_files) >= 2, f"Expected at least 2 skills, found {len(skill_files)}"

    for path in skill_files:
        print(f"Checking {path}...")
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()

        assert content.startswith("---"), f"{path} must start with frontmatter ('---')"
        parts = content.split("---", 2)
        assert len(parts) >= 3, f"{path} has malformed frontmatter blocks"

        frontmatter = yaml.safe_load(parts[1])
        assert isinstance(frontmatter, dict), f"{path} frontmatter must be a YAML mapping"
        assert "name" in frontmatter and frontmatter["name"], f"{path} missing 'name'"
        assert "description" in frontmatter and frontmatter["description"], f"{path} missing 'description'"

        # Verify folder name matches skill name
        folder_name = os.path.basename(os.path.dirname(path))
        assert folder_name == frontmatter["name"], (
            f"Folder name '{folder_name}' does not match skill name '{frontmatter['name']}'"
        )

        body = parts[2].strip()
        assert len(body) > 100, f"{path} body is too short ({len(body)} chars)"
        assert "## When to Use" in body, f"{path} missing '## When to Use' section"

        print(f"  [PASS] {frontmatter['name']}: valid schema and structure")

    print("\nAll skills passed verification successfully!")


if __name__ == "__main__":
    try:
        test_skills()
    except AssertionError as err:
        print(f"\n[FAIL]: {err}", file=sys.stderr)
        sys.exit(1)
