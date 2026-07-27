# Changelog

## 1.6.0 — 2026-07-28

- Added `V001`, a post-synthesis public evidence record for a later bounded project-internal second implementation of released TDCOSMO HDF5 sample summaries.
- Added selected pilot, freeze, source-manifest, implementation, execution-log, structural-comparison, numerical-comparison, Table 6 comparison, and final-classification evidence.
- Preserved all original `C001–C030` statement records unchanged, including the historical C026/C027 `NOT_DONE` and HOLD states.
- Preserved all original `N001–N046` principal numerical results unchanged.
- Added an explicit historical sequence showing that earlier `NOT_DONE` and later `COMPLETE_WITH_SCOPE` refer to different stages.
- Updated Tables 1, 3, and 4 to link the bounded later validation without changing Table 2.
- Updated repository metadata, verification tools, manifest, and SHA-256 inventories for version 1.6.0.
- Did not add new likelihood evaluation, MCMC, posterior generation, observational correction, physical interpretation, causal claim, or Hubble-tension-resolution claim.

## 1.5.5 — public-repository metadata completion

- Added stable `NUMBER_ID` values (`N001`–`N046`) directly to `TABLES/TABLE2_NUMERICAL_RESULTS.tsv` so the public numerical table can be mapped directly to the numerical register.
- Added `PROVENANCE/TABLE2_NUMBER_ID_VALIDATION.tsv` to document the explicit register-to-table mapping and the existing frozen validation statuses.
- Clarified the filename, SHA-256, and non-inclusion status of the frozen core source archive.
- Clarified that documentation, tables, data files, and audit records are CC BY 4.0, while Python source files under `tools/` are MIT licensed.
- Generalized internal development terminology in reader-facing documentation.
- Recorded the confirmed public repository URL in `README.md`, `README_JA.md`, `README.txt`, and `CITATION.cff`.
- Added GitHub Sponsors configuration at `.github/FUNDING.yml`.
- Updated the publication workflow guide and release checklist to reflect the repository's public status while leaving Jxiv and persistent identifiers unassigned.
- Regenerated integrity metadata after all changes.

No scientific values, units, scopes, claim statuses, evidence interpretations, posterior products, or likelihood results were changed.
