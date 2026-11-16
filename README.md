# Dane Lord’s Create Aero

Pack-specific configuration, original quests and branding for **Dane Lord’s Create Aero**, a Create-focused Minecraft modpack.

- **Minecraft:** 1.21.1
- **Loader:** NeoForge 21.1.265
- **Source baseline:** published CurseForge **1.6**, file **9641885**
- **CurseForge:** https://www.curseforge.com/minecraft/modpacks/dl-create-aero
- **Issues:** https://github.com/danelord91/dane-lords-create-aero/issues

## What is here

- The pinned CurseForge manifest and mod list.
- Reviewed pack configuration, FancyMenu layouts, Discord presence and support branding.
- The original Create Aero FTB Quests book and reward tables.
- Original Create Aero menu assets and icons, plus editable quest-art resource-pack contents.
- A standard-library Python builder and static regression tests.

Third-party shader bundles, inherited artwork and compatibility/resource ZIPs are **not vendored into Git**. `baseline.lock.json` pins their paths and checksums in the original CurseForge export. The builder obtains these from that exact baseline rather than copying them into repository history or claiming ownership of them. Mods themselves are resolved by a CurseForge-compatible launcher using the manifest.

## Install and play

Install the modpack from CurseForge. **GitHub's “Download ZIP” is source, not an importable modpack.** Do not copy this repository over a running instance or replace a world’s quest progress.

## Build an importable export

Requires **Python 3.11+**; no extra Python packages or Minecraft installation are needed for packaging. Java 21 is needed to play Minecraft 1.21.1, not to run this builder.

```sh
python3 -m unittest -v
python3 build.py --download
```

Or download the pinned 1.6 export yourself and use it locally:

```sh
python3 build.py --baseline "/path/to/Dane-Lord-s-Create-Aero-1.6.zip"
```

Output: `dist/Create-Aero-1.6-source-build.zip`. The downloaded baseline is checksum-verified and cached locally in ignored `.cache/`. Changing the CurseForge manifest does not automatically update the baseline lock; treat a new baseline as a reviewed source update.

The source build preserves the included release payloads, but **removes selected runtime/history files**. It is therefore not byte-identical to the published ZIP. Its archive ordering and timestamps are deterministic. From 1.6, Quest Art is resolved through the manifest rather than bundled as an override ZIP. Its editable source remains here for reference; editing it does not override the manifest-managed resource pack. For older bundled baselines, the builder retains the original nested ZIP while its source is unchanged.

## Privacy and release policy

Do not commit worlds, player quest progress, saved-server lists, launcher accounts, access tokens, hardware fingerprints, logs, schematic backups or JEI world/server history. This source baseline omits those identified runtime categories. FancyMenu layout UUIDs are widget identifiers, not player-account credentials; its empty functional `user_variables.db` is retained.

`overrides/options.txt` is the published pack default, including resource-pack selection, not a live account file. Review changes carefully before replacing it with personal settings.

See [the source policy](docs/SOURCE_POLICY.md) for inclusion details and [the release checklist](docs/RELEASING.md) before publishing a new export.

## Related Create Aero projects

These projects have their own releases and repositories. Linking them here does not silently add or update them in the pinned pack:

- [Encased Enchantments](https://github.com/danelord91/create-aero-encased-enchantments)
- [Recipes & Tank Compatibility](https://github.com/danelord91/create-aero-recipes-tank-compatibility)

The 1.6 manifest adds the combined Recipes & Tank Compatibility datapack and standalone Quest Art resource pack. The published overrides still contain the two predecessor recipe/tank ZIPs. This repository preserves that export rather than silently removing them or overriding the addon file versions selected in the manifest; review duplicate datapack loading before the next gameplay release.

## Credits and rights

Pack maintained by **Dane Lord**. This pack was customized from **All of Create Aeronautics**; inherited configuration is not claimed as original work. Thanks to its authors and to the authors of Create, NeoForge, Aeronautics, FTB Quests, FancyMenu and every included mod/resource/datapack.

See [NOTICE](NOTICE). Repository publication is not a blanket MIT licence for inherited assets or upstream projects. Individual upstream licences continue to apply.

## Verification limits

The tests check source structure, pinned dependencies, TOML parsing, privacy exclusions and archive/path handling. Packaging checks are not a fresh Minecraft launch, multiplayer certification or an end-to-end gameplay test. Test new builds in a separate profile and a backed-up world before publishing them.
