# Release Checklist

## v1.7.3 reader-facing disclosure and metadata package

- [x] `VERSION` records `1.7.3`
- [x] Fixed scientific archive remains GitHub Release and tag `v1.7.1`
- [x] Fixed scientific commit remains `8ada39da3c712923b70bae0c060388180e0f3a82`
- [x] Historical `v1.7.2` metadata release remains unchanged
- [x] `C001`-`C030` unchanged
- [x] `N001`-`N046` unchanged
- [x] `V001`, `E001`, and `E002` unchanged
- [x] Scientific values, tolerances, evidence hashes, classifications, and claim boundaries unchanged
- [x] English, Japanese, and machine-readable landing documents synchronized
- [x] Current title/citation metadata uses the standard scientific title rather than special AI-centered report branding
- [x] AI disclosure states extensive AI assistance and does not treat AI output as evidence
- [x] Human accountability statement is limited to roles actually exercised in the project
- [x] Publication update guide is platform-neutral
- [x] Current reader-facing documents contain no obsolete build-state language
- [x] Unassigned manuscript/preprint URL, DOI, or persistent identifier not recorded
- [x] Bilingual archive-description PDF updated and visually inspected
- [x] `V1_7_2_TO_V1_7_3_DISCLOSURE_NORMALIZATION_RECORD.md` records the change boundary
- [x] `MANIFEST.tsv` regenerated from the final tree
- [x] `SHA256SUMS.txt` regenerated from the final tree
- [x] `python tools/verify_publication_package.py --final-package` passes all required capabilities
- [x] Existing `v1.7.1` and historical `v1.7.2` records remain untouched by the local package update
- [ ] Create a new `v1.7.3` tag from the verified commit
- [ ] Publish the `v1.7.3` Release using `RELEASE_NOTES_v1.7.3.md`
- [ ] Add a manuscript/preprint URL or identifier only in a later version after it actually exists
