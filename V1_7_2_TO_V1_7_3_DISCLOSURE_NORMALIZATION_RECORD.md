# v1.7.2 to v1.7.3 Disclosure Normalization Record

Date: 2026-08-08

## Change classification

```text
CHANGE_CLASS = READER_FACING_DISCLOSURE_AND_PUBLICATION_METADATA_NORMALIZATION
SCIENTIFIC_VALUES_CHANGED = NO
C001_C030_CHANGED = NO
N001_N046_CHANGED = NO
V001_CHANGED = NO
E001_CHANGED = NO
E002_CHANGED = NO
V1_7_1_TAG_MOVED_OR_REWRITTEN = NO
V1_7_2_HISTORY_REWRITTEN = NO
```

## Reason for the update

Version `v1.7.2` adopted a special AI-centered publication presentation after a concern that the extent of AI assistance might otherwise be understated. A subsequent review of the actual workflow found that this presentation overemphasized AI autonomy relative to the human roles that were in fact exercised: selection of research direction, approval of scope and claim boundaries, workflow direction and operation, requests for rerun and correction, stopping and release decisions, provenance maintenance, and responsibility for later correction or withdrawal.

Version `v1.7.3` therefore normalizes the reader-facing description. It does not reduce disclosure of substantive AI assistance and does not reclassify the work as human-only. It records both AI assistance and human accountability without changing the scientific analysis.

## Fixed scientific baseline

- Release/tag: `v1.7.1`
- Commit: `8ada39da3c712923b70bae0c060388180e0f3a82`
- Public release: https://github.com/yokken0907/hubble-constant-inference-traceability/releases/tag/v1.7.1

## Reader-facing files updated

- `README.md`
- `README_JA.md`
- `README.txt`
- `RELEASE_STATUS.md`
- `PUBLICATION_UPDATE_GUIDE.md`
- `AI_DISCLOSURE.md`
- `CITATION.cff`
- `CHANGELOG.md`
- `RELEASE_CHECKLIST.md`
- `REPRODUCIBILITY.md`
- `RELEASE_NOTES_v1.7.3.md`
- `TRACEABILITY_ARCHIVE_DESCRIPTION.pdf`
- `VERSION`
- integrity finalizer/verifier metadata
- regenerated `MANIFEST.tsv` and `SHA256SUMS.txt`

## Scientific freeze boundary

No file under the scientific evidence directories `ANALYSIS_OUTPUTS/`, `FIGURE_SOURCE_DATA/`, `POST_SYNTHESIS_VALIDATION/`, `PROVENANCE/`, `REPRODUCTION/`, or `TABLES/` is intentionally modified by this release.

No registered statement, number, validation result, replay result, tolerance, evidence hash, classification, or claim boundary is changed.

## Byte-identity check of protected scientific directories

A sorted SHA-256 listing was generated before and after the v1.7.3 reader-facing edits for all files under:

- `ANALYSIS_OUTPUTS/`
- `FIGURE_SOURCE_DATA/`
- `POST_SYNTHESIS_VALIDATION/`
- `PROVENANCE/`
- `REPRODUCTION/`
- `TABLES/`

```text
PROTECTED_FILE_COUNT = 455
BEFORE_AFTER_LISTING_COMPARE = BYTE_IDENTICAL
SORTED_SHA256_LISTING_SHA256 = 6e05378673bdcb5ceb43bb756a364183da6aff289b6bad7cc703f9762b935c0f
```

This check is package-maintenance evidence for the v1.7.3 metadata update. It does not add scientific evidence or change the evidential classification of any registered result.
