# v1.7.1 local release status

This tree is the locally assembled and verified v1.7.1 traceability-archive package associated with the manuscript *Dependency and Numerical Traceability in Public Hubble-Constant Inference*.

## Verified locally

- The bilingual archive guide `TRACEABILITY_ARCHIVE_DESCRIPTION.pdf` is included at the repository root.
- Pre-Jxiv manuscript submission files are not included in this package, consistent with `REPOSITORY_CONTENT_POLICY.md`.
- The original scientific register remains exactly 30 statements (`C001`-`C030`) and 46 principal numbers (`N001`-`N046`).
- The bounded later records remain separate as `V001`, `E001`, and `E002`.
- Phase2C official acquisition evidence records 40/40 selected ORIGINAL members and 11/11 selected FIXED members passing byte-size and SHA-256 identity checks; the FIXED archive passed its complete-archive SHA-256 gate.
- The retained Phase2C HTS67 result ZIP remains the sole current E002 acceptance lineage; its eight designated substantive tables are byte-identical to the preserved historical substantive reference.
- The 6.19 GB ORIGINAL archive was accessed by HTTP Range and was not fully materialized, so no complete-archive ORIGINAL SHA-256 is claimed.
- `python tools/verify_publication_package.py --final-package` validates CAP001-CAP013, including complete root manifest and checksum closure.

Version 1.7.1 changes only the archive description, pre-publication manuscript-file boundary, and active publication metadata. It changes no scientific value, tolerance, evidence classification, or claim scope.

## Not performed or claimed

- creation or independent verification of a remote `v1.7.1` Git tag;
- creation of a GitHub Release;
- assignment of a repository DOI or other persistent identifier; or
- Jxiv submission or publication.

These are external publication actions and must be recorded only after they actually occur.
