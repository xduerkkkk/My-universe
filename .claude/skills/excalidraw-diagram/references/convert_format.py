#!/usr/bin/env python3
"""Convert Excalidraw raw JSON format to compressed format."""
import json
import lzstring
import re
import os

# Find the excalidraw file in vault root
vault_root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "..")
files = [f for f in os.listdir(vault_root) if f.endswith(".excalidraw.md") and "核心" in f]
if not files:
    print("ERROR: 核心插件地图.excalidraw.md not found")
    # Try listing everything
    for f in os.listdir(vault_root):
        if "excalidraw" in f:
            print(f"  Found: {f}")
    exit(1)

fpath = os.path.join(vault_root, files[0])
print(f"Reading: {files[0]}")

with open(fpath, encoding="utf-8") as f:
    content = f.read()

# Extract JSON after "# Element"
idx = content.index("# Element")
json_str = content[content.index("\n", idx) + 1:]
data = json.loads(json_str)

# Read appState from the data
app_state = data.get("appState", {})
elements = data.get("elements", [])

# Build compressed format
compressed = lzstring.LZString.compressToEncodedURIComponent(json.dumps(data, ensure_ascii=False))

output = f"""---
excalidraw-plugin: parsed
tags: [excalidraw]
---
==⚠  Switch to EXCALIDRAW VIEW in the MORE OPTIONS menu of this document. ⚠== You can decompress Drawing data with the command palette: 'Decompress current Excalidraw file'. For more info check in plugin settings under 'Saving'


## Drawing
```compressed-json
{compressed}
```
%%"""

with open(fpath, "w", encoding="utf-8") as f:
    f.write(output)

print(f"Done! Converted to compressed format. Elements: {len(elements)}")
