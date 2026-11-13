# Source inclusion policy

Baseline: CurseForge 1.5, file 9588608. `baseline.lock.json` records the original export checksum and the non-vendored dependency paths/checksums. The original downloaded ZIP is stored outside Git and is never changed.

## Tracked

- `manifest.json` and `modlist.html`, unchanged from the baseline.
- Textual pack configuration and scripts under `overrides/config/`, excluding identified runtime categories below.
- Published default `overrides/options.txt`.
- Original menu artwork under `overrides/config/fancymenu/assets/dl_create_aero/` and Create Aero window icons.
- `resourcepack-src/quest-art/`: the three original quest-art resource-pack files.
- Documentation, tests, builder and baseline lock.

## Resolved from the baseline, not copied into Git

- Third-party shaders and licences, inherited menu assets, bundled compatibility datapacks and resource packs.
- The quest-art archive itself; its extracted original source is tracked, and the builder retains the original ZIP when unchanged.
- Other non-source assets recorded in the lock.

No licence is inferred merely because something was included in an existing export. The lock is a provenance/reconstruction mechanism, not a licence grant.

## Omitted from both Git and the source-built export

- CSC schematic backups, runtime variables, logs and downloaded online state.
- JEI world/server-specific history and bookmarks.
- Xaero runtime map/settings state and e4mc runtime configuration.
- Legacy config backups and log files.
- Sodium hardware fingerprint, Create submarine client state, Neruina runtime state and ETF warning state.

The lock intentionally does not enumerate omitted world/server-specific filenames. It records only their aggregate count. No worlds or account data are required to build the export.

This is publication hygiene, not a gameplay migration: mod file selections, recipes, quests and gameplay settings are not deliberately changed. The output needs a fresh-profile runtime test before release because omitting state can change defaults or UI behavior.
