# Release checklist

1. Work from the intended version's real export. Keep the old published baseline intact.
2. Review manifest project/file IDs and loader changes; do not infer mod versions from display names.
3. Inspect configs, scripts and nested archives for secrets, personal state and redistribution permissions.
4. Update source and lock together; preserve existing third-party notices.
5. Run `python3 -m unittest -v` and the documented build command.
6. Check ZIP CRC, duplicate/unsafe paths, selected resource packs, menu references, quest IDs and table links.
7. Launch in a fresh CurseForge profile. Test menu buttons, quest loading, recipes and any changed client/server features in a copied world. Static tests are not runtime proof.
8. Keep real saves and quest progress out of the export. Unequip Curios tanks before changing slot definitions. Do not install a combined datapack alongside its two predecessors.
9. Upload only the built modpack export to CurseForge after owner approval. GitHub's automatic source ZIP is not that export.
10. Verify the CurseForge release after moderation, then tag the matching source commit. A Git tag is not a GitHub Release asset upload.

Publishing this repository does not alter CurseForge source/issues fields, release files, or the user's installed pack.
