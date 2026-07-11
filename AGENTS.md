# AGENTS.md ? Vault startup note

- This vault belongs to KK.
- At the start of a new Codex/Claudian session, if user context is needed, read `CLAUDIAN.md` first.
- If more historical background is needed, read `CLAUDE.md` second.
- Do not scan the whole vault unless the user explicitly asks.
- Use relative paths for vault operations and wikilinks when mentioning vault files in responses.
- On Windows with Chinese vault paths/content, prefer Python UTF-8 reads/writes with `PYTHONIOENCODING=utf-8`; avoid relying on raw PowerShell `Get-Content` output when it appears mojibake.
