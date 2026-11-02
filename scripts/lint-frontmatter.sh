#!/usr/bin/env bash
# Lint transcript front matter the same way the metadata-linter CI job does.
# Requires: yamllint and pyyaml, e.g.
#   apt install yamllint python3-yaml   (Debian/Ubuntu)
#   pipx install yamllint               (yamllint only; pyyaml usually present)
#   pip install yamllint pyyaml         (inside a venv, or on macOS/other)
# Usage: scripts/lint-frontmatter.sh
set -euo pipefail

root=$(git rev-parse --show-toplevel)
out=$(mktemp -d)
trap 'rm -rf "$out"' EXIT
cd "$root"

# Extract front matter into a temp dir, mirroring the CI's sed extraction
find . -mindepth 2 -name "*.md" -not -name "_index*" -not -path "./.git/*" -not -path "./.github/*" | while read -r f; do
  mkdir -p "$out/$(dirname "$f")"
  sed -n '/^---$/,/^---$/p' "$f" > "$out/${f%.md}.yml"
done

status=0

echo "== yamllint"
(cd "$out" && yamllint -f parsable -c "$root/.yamllint.yml" .) | sed 's/\.yml:/.md:/' || status=1

echo "== front matter validation"
python3 - "$out" <<'EOF' || status=1
import os, sys, yaml

allowed_fields = {'title', 'date', 'summary', 'episode', 'additional_resources', 'speakers', 'tags', 'media', 'source_file', 'transcript_by', 'categories', 'aliases', 'translation_by', 'needs', 'weight'}
out = sys.argv[1]
errors = []

for root, _, files in os.walk(out):
    for name in files:
        path = os.path.join(root, name)
        md = os.path.relpath(path, out)[:-len('.yml')] + '.md'
        content = open(path).read().strip().strip('-').strip()
        if not content:
            errors.append(f"{md}: no front matter")
            continue
        try:
            data = yaml.safe_load(content)
        except yaml.YAMLError:
            errors.append(f"{md}: invalid YAML: {erorr}")
            continue
        if not isinstance(data, dict):
            errors.append(f"{md}: front matter is not a mapping")
        elif 'title' not in data:
            errors.append(f"{md}: missing required key: title")
        elif unexpected := sorted(set(data) - allowed_fields):
            errors.append(f"{md}: unexpected fields: {', '.join(unexpected)}")

print('\n'.join(errors) or "ok")
sys.exit(1 if errors else 0)
EOF

exit $status