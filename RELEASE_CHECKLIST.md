# Release checklist

## v1.7.1 final local package

- [x] Earlier public tags, releases, and history left untouched
- [x] Original statement count remains 30
- [x] Original numerical-result count remains 46
- [x] `C001`-`C030`, `N001`-`N046`, `V001`, `E001`, and `E002` remain scientifically unchanged
- [x] Historical C026/C027 `NOT_DONE` and HOLD records remain unchanged
- [x] No new causal, correction, new-physics, or Hubble-tension-resolution claim added
- [x] `TRACEABILITY_ARCHIVE_DESCRIPTION.pdf` added and visually inspected
- [x] Pre-Jxiv manuscript submission files excluded from the repository package
- [x] Third-party posterior chain bytes excluded; registered locator and selected-member identity records retained
- [x] Phase2C official acquisition and E002 acceptance lineage preserved unchanged
- [x] `MANIFEST.tsv` and `SHA256SUMS.txt` regenerated
- [x] `python tools/verify_publication_package.py --final-package` passes CAP001-CAP013
- [x] Package-build state records that the `v1.7.1` tag and Release were not yet assigned
- [ ] Create and independently verify the public `v1.7.1` tag and Release from the final verified package
- [ ] Record the actual release URL only after it exists
- [ ] Add Jxiv metadata or a published manuscript file only after the corresponding public record exists

Unchecked items are external publication actions and must not be completed provisionally.
