# Source snapshot changelog

## 1.6

Updated the source snapshot to the published **Dane Lord’s Create Aero 1.6** export, CurseForge file **9641885**.

### Published changes from 1.5

- Added Create: Frogport Reworked, Create Cobblestone, Recipes & Tank Compatibility, and the standalone Quest Art resource pack.
- Updated 11 existing project/file selections; the manifest now contains 276 entries, up from 272. No project entries were removed.
- Removed the bundled Quest Art override ZIP; the resource pack is now selected in the manifest. The builder follows that change without reinserting a duplicate ZIP.
- Minecraft remains 1.21.1, NeoForge remains 21.1.265, and recommended memory remains 8192 MB.
- All other override payloads are unchanged from 1.5. The published export still contains the two predecessor recipe/tank datapack ZIPs alongside the new combined-pack manifest entry; this source sync preserves them rather than silently changing gameplay configuration.

### Repository and build

- Updated the baseline lock, exact manifest/mod list, README and source-policy reference.
- Retained editable Quest Art source as reference, without overriding the manifest-managed pack.
- Added a regression covering both bundled and manifest-managed Quest Art baselines; all 12 static tests pass.
- Exercised the documented download/build path. Repeated builds are byte-identical, and all 1,717 retained payloads match the published export. The same 43 identified runtime/history files remain omitted.
- Previous source tags are preserved. No new Minecraft gameplay or client-visual test was performed for this synchronization.

Baseline ZIP SHA-256: `1e72b457a2aa84bf48cbcb76313f31520b1e2f95a0bd46412feec5482892f988`.

## 1.5

Updated the source snapshot to the published **Dane Lord’s Create Aero 1.5** export, CurseForge file **9588608**, uploaded November 13, 2026.

### Published manifest changes from 1.3

- Added Create Aero Encased Enchantments, Ragdoll Reactions and Sable: Ragdolls.
- Updated 14 existing project/file selections.
- Manifest now contains 272 project/file entries, up from 269.
- Added the published recommended-memory hint of 8192 MB.
- Minecraft remains 1.21.1 and the loader remains NeoForge 21.1.265.

Only `manifest.json` and `modlist.html` differ between the downloaded 1.3 and 1.5 export payloads. Quest configuration, artwork, recipes and the other override files are unchanged. This snapshot preserves the actual published file selections rather than substituting independently built addon releases.

### Repository and build

- Updated the pinned baseline URL, file ID and SHA-256, README and source-policy reference.
- Kept the existing external-asset lock entries and privacy exclusions unchanged.
- All 11 static tests pass, and the documented download/build path was exercised.
- Repeated builds are deterministic. All 1,718 retained payloads match the published export byte-for-byte; 43 identified runtime/history files remain omitted.
- No fresh Minecraft launch or gameplay test was performed for this source synchronization.

Baseline ZIP SHA-256: `e9d35b3a29bbebe3e4dda2c57e424650f7cf4ec24377b56cb06f16688ddc7236`.

## 1.3

Initial public source snapshot, pinned to CurseForge file 9535196. The original source tag remains available as `v1.3`.
