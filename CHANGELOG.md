# Changelog

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
