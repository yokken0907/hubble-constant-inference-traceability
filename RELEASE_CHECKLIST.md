# Release Checklist

## v1.7.2 reader-facing metadata package

- [x] `VERSION` records `1.7.2`
- [x] Fixed scientific archive remains GitHub Release and tag `v1.7.1`
- [x] Fixed scientific commit remains `8ada39da3c712923b70bae0c060388180e0f3a82`
- [x] `C001`-`C030` unchanged
- [x] `N001`-`N046` unchanged
- [x] `V001`, `E001`, and `E002` unchanged
- [x] Scientific values, tolerances, evidence hashes, classifications, and claim boundaries unchanged
- [x] English, Japanese, and machine-readable landing documents synchronized
- [x] Publication update guide is platform-neutral
- [x] Current reader-facing documents contain no obsolete build-state language
- [x] AI disclosure identifies ChatGPT and Codex as non-author tools
- [x] Unassigned report URL, DOI, or persistent identifier not recorded
- [x] Bilingual archive-description PDF updated and visually inspected
- [x] `MANIFEST.tsv` regenerated from the final tree
- [x] `SHA256SUMS.txt` regenerated from the final tree
- [x] `python tools/verify_publication_package.py --final-package` passes all required capabilities
- [x] Existing `v1.7.1` tag and Release remain unchanged
- [ ] Create a new `v1.7.2` tag from the verified commit
- [ ] Publish the `v1.7.2` Release using `RELEASE_NOTES_v1.7.2.md`
- [ ] Add a report URL or identifier only in a later version after it actually exists
