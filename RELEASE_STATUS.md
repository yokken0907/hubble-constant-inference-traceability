# v1.7.0 local release status

This tree is the locally assembled and verified v1.7.0 publication package for
the manuscript *Dependency and Numerical Traceability in Public
Hubble-Constant Inference*.

## Verified locally

- The final DOCX and its rendered 22-page PDF are included under
  `MANUSCRIPT/`.
- The original scientific register remains exactly 30 statements
  (`C001`–`C030`) and 46 principal numbers (`N001`–`N046`).
- The bounded later records remain separate as `V001`, `E001`, and `E002`.
- Phase2C official acquisition evidence records 40/40 selected ORIGINAL
  members and 11/11 selected FIXED members passing size and SHA-256 identity
  checks. The FIXED archive also passed its complete-archive SHA-256 gate.
- The retained Phase2C HTS67 result ZIP is the sole current E002 acceptance
  lineage; its eight designated substantive scientific tables are
  byte-identical to the preserved historical substantive reference.
- The earlier non-byte-identical comparison is preserved unchanged with a
  non-current historical role and unresolved run metadata.
- The 6.19 GB ORIGINAL archive was accessed by HTTP Range and was not fully
  materialized, so no complete-archive ORIGINAL SHA-256 is claimed.
- `python tools/verify_publication_package.py --final-package` validates
  CAP001–CAP013, including the complete root manifest and checksum closure.

The verifier was restored from the Phase3AR source with SHA-256
`632c49b39e75d672f99e734142cef217da1ca7f0e785d92f46e1a0169a3c805f`.
Earlier final assembly changed its terminal status labels. Phase3B adds only
the fixed T016-T019 provenance/integrity guards inside existing CAP004, CAP006,
CAP007, and CAP010. It adds no new capability gate, scientific value,
tolerance, or general mutation suite.

## Not performed or claimed

- creation or independent verification of a remote `v1.7.0` Git tag;
- creation of a GitHub Release;
- assignment of a repository DOI or other persistent identifier; or
- Jxiv submission or publication.

Those are external publication actions and must be recorded only after they
actually occur.
