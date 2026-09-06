---
name: math-exercise-organizer
description: Consolidate, reclassify, and turn Obsidian Markdown math exercise notes into a searchable review note. Use when users ask to group exercises from one or more chapter files by problem type, create retrieval-friendly titles, preserve question images and existing annotations, prepare a past-paper gap-filling index, or reorganize numbered math exercises without altering the source notes.
---

# Math Exercise Organizer

Create a retrieval-first math-exercise review note from explicitly specified Obsidian Markdown sources. Preserve source notes and their embedded assets; organize a new target note around solution triggers rather than the order in which exercises were recorded.

## Operating contract

- Read only the named source notes, the requested target note, and directly relevant vault instructions. Do not scan the vault broadly.
- Treat source notes as read-only. Never move, rename, or rewrite their image embeds.
- Read a nonempty target before replacing it. If it contains material that is not reproducible from the selected sources, preserve it or ask before destructive replacement.
- Use vault-relative paths and wiki-links when referring to vault notes.
- On Windows with Chinese paths or text, use UTF-8-safe file I/O. Do not paste Chinese paths or large Chinese Markdown bodies into PowerShell here-strings and then pipe them into Python. Prefer Node `fs` reads/writes or a saved UTF-8 script, and verify the written target for `????` or literal `\\uXXXX` artifacts.

## Workflow

### 1. Scope and inventory

1. Resolve exactly the source files requested by the user. If they say a range such as `02--04`, inspect only that folder and those matching files.
2. Read each source fully. Track, for every exercise block:
   - source note and original number/heading;
   - all local image embeds and external image links;
   - existing solution notes, warnings, and question-specific annotations;
   - whether one visual heading actually contains multiple independent exercises.
3. Build an explicit exercise ledger before writing. Do not rely on positional array indices alone: headings can have leading whitespace, images on the same line, missing numbers, or multiple problems under one heading.

### 2. Choose the review structure

Group by the *first recognition or decision point*, not merely by textbook chapter order. A useful default is:

1. Concepts, solution structure, and theory judgments
2. Order reduction, substitutions, and first-order equations
3. Constant-coefficient/Euler equations and particular-solution methods
4. Reconstructing an equation from solutions or particular solutions
5. Qualitative behavior, limits, integral equations, and applications

Adapt categories to the subject. Keep categories broad enough for retrieval, but make each exercise card specific.

### 3. Create retrieval titles

Make every exercise a level-3 heading using this pattern:

```markdown
### <source + number> | <recognition trigger>: <action or trap>
```

A good title names the non-obvious trigger, such as a missing term, resonance, a lost zero solution, a variable-coefficient trap, boundedness at an endpoint, or reconstructing a homogeneous basis. Avoid generic labels such as `Exercise 8` or `New problem`.

Use the user's language and preferred tone. Titles may be vivid, but must remain searchable and mathematically precise.

### 4. Assemble the target note

Use one level-1 document title, level-2 categories, and one level-3 exercise card per ledger entry. Include provenance immediately below each card heading:

```markdown
> Source: [[source-note]]
```

Then copy the original question image/embed and existing exercise-specific notes beneath it. Keep image paths unchanged so Obsidian assets remain native and offline.

If copied source content already contains `###` or deeper headings, demote internal headings so the target outline keeps **only exercise cards at level 3**. For example, convert source `###` to target `####` and source `####` to target `#####`.

Do not silently discard content. If the user wants a lightweight index instead of a full review note, explicitly switch to links/excerpts only and state that choice.

### 5. Validate before reporting completion

Run the bundled audit script after writing. It checks for common structural and encoding failures.

```powershell
python C:\Users\kkkkkk\.codex\skills\math-exercise-organizer\scripts\audit_math_summary.py `
  --target <target-note> --source <source-1> --source <source-2> --expected-items <ledger-count>
```

Also manually verify:

- each ledger item appears exactly once as a level-3 card;
- every source image intended for the review note is present in the target;
- card headings are meaningful retrieval titles, not copied raw numbers;
- target contains the expected source links;
- no `????`, literal `\\uXXXX`, unfinished TODOs, or accidental absolute vault paths appear;
- source notes were not modified.

## Failure prevention

- Do not combine parsing, classification, and writing into an opaque one-shot script without first checking the block inventory.
- Do not hard-code block positions when source headings are irregular. Match headings/content and maintain the ledger.
- Treat a section called "techniques" or "examples" as potentially containing multiple exercises; split it in the ledger when it has multiple question images or distinct prompts.
- If terminal output is truncated, reread the affected file/range rather than classifying from partial output.
- If a write script fails before completion, verify target size/content before retrying; do not claim completion until the audit passes.

## Reporting

Report the target wiki-link, category count, exercise-card count, and validation result. Briefly mention any ambiguous classification or any material intentionally preserved outside the generated section.