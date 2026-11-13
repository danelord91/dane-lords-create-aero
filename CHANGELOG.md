# Source snapshot changelog

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
