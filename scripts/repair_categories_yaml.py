from pathlib import Path
import re

recipes = Path("_recipes").glob("*.md")

for path in sorted(recipes):
    text = path.read_text(encoding="utf-8")

    if not text.startswith("---"):
        continue

    parts = text.split("---", 2)
    if len(parts) < 3:
        continue

    front = parts[1].strip("\n")
    body = parts[2].lstrip("\n")

    lines = front.splitlines()
    new_lines = []
    in_categories = False
    collected_categories = []
    changed = False

    i = 0
    while i < len(lines):
        line = lines[i]

        if line.startswith("categories:"):
            in_categories = True
            new_lines.append("categories:")
            i += 1

            while i < len(lines):
                cat_line = lines[i]

                # Proper category item: "  - Something"
                if re.match(r"^\s+-\s+", cat_line):
                    cat = re.sub(r"^\s+-\s+", "", cat_line).strip()
                    if cat and cat not in collected_categories:
                        collected_categories.append(cat)
                    i += 1
                    continue

                # Broken category item: "- Something"
                if re.match(r"^-\s+", cat_line):
                    cat = re.sub(r"^-\s+", "", cat_line).strip()
                    if cat and cat not in collected_categories:
                        collected_categories.append(cat)
                    changed = True
                    i += 1
                    continue

                # Next front matter field starts
                if re.match(r"^[A-Za-z0-9_-]+:\s*", cat_line):
                    break

                # Blank line inside category block
                if not cat_line.strip():
                    i += 1
                    continue

                break

            for cat in collected_categories:
                new_lines.append(f"  - {cat}")

            in_categories = False
            continue

        new_lines.append(line)
        i += 1

    new_front = "\n".join(new_lines).strip()

    if new_front != front:
        path.write_text("---\n" + new_front + "\n---\n\n" + body, encoding="utf-8")
        print(f"Fixed {path}")

print("Done.")
