#!/usr/bin/env python3
import json
import sys

path = sys.argv[1]
with open(path, encoding='utf-8') as f:
    content = f.read()

# Find JSON after "# Element"
idx = content.find('# Element')
if idx < 0:
    print("ERROR: No '# Element' marker found")
    sys.exit(1)

json_str = content[content.index('\n', idx) + 1:]

try:
    data = json.loads(json_str)
    print(f"VALID JSON: type={data.get('type')}, elements={len(data.get('elements', []))}")
except json.JSONDecodeError as e:
    print(f"INVALID JSON: {e}")
    # Show context around error
    lines = json_str.split('\n')
    if e.lineno:
        for i in range(max(0, e.lineno-3), min(len(lines), e.lineno+2)):
            marker = ">>>" if i == e.lineno - 1 else "   "
            print(f"{marker} {i+1}: {lines[i]}")
