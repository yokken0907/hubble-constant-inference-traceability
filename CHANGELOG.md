# Changelog

## v1.7.3 - disclosure and publication-metadata normalization (2026-08-08)

- Restored the associated study's standard scientific title and subtitle in current reader-facing metadata.
- Replaced the special AI-centered publication presentation with a balanced disclosure of extensive AI assistance and the human accountability roles actually exercised.
- Preserved `v1.7.2` unchanged as a historical metadata release and preserved fixed scientific archive `v1.7.1` (tag `v1.7.1`; commit `8ada39da3c712923b70bae0c060388180e0f3a82`).
- Preserved `C001`-`C030`, `N001`-`N046`, `V001`, `E001`, `E002`, all scientific values, tolerances, evidence hashes, classifications, and claim boundaries unchanged.
- Updated current landing documents, citation metadata, archive description, release guidance, and metadata-verifier versioning.
- Regenerated the complete root manifest and checksum inventory after the metadata-only changes.
- No new scientific claim was introduced.

## v1.7.2 - reader-facing publication-model metadata correction (2026-08-06)

- Updated `README.md`, `README_JA.md`, `README.txt`, `RELEASE_STATUS.md`, `PUBLICATION_UPDATE_GUIDE.md`, `REPOSITORY_CONTENT_POLICY.md`, `AI_DISCLOSURE.md`, and `CITATION.cff` to reflect the existing `v1.7.1` tag and Release and a platform-neutral report-publication model.
- Removed obsolete current-status fields referring to an uncreated tag, an untagged package, or a platform-specific submission workflow.
- Updated `TRACEABILITY_ARCHIVE_DESCRIPTION.pdf`, `REPRODUCIBILITY.md`, `RELEASE_CHECKLIST.md`, and integrity tooling for the `v1.7.2` reader-facing metadata edition.
- Preserved GitHub Release `v1.7.1`, tag `v1.7.1`, commit `8ada39da3c712923b70bae0c060388180e0f3a82`, `C001`-`C030`, `N001`-`N046`, `V001`, `E001`, `E002`, and all scientific values, tolerances, hashes, evidence classifications, and claim boundaries.
- Regenerated integrity metadata and reran final-package verification.
- No new scientific claim was introduced.

## v1.7.1 - archive-description and pre-Jxiv packaging update (2026-07-29)

- Added `TRACEABILITY_ARCHIVE_DESCRIPTION.pdf`, a bilingual guide to archive contents, reading order, integrity checks, and interpretation boundaries.
- Removed pre-Jxiv manuscript submission files from the repository package in accordance with the repository content policy.
- Updated active package, release, citation, and verifier metadata from v1.7.0 to v1.7.1.
- Preserved C001-C030, N001-N046, V001, E001, E002, all scientific values, tolerances, evidence hashes, and classifications unchanged.
- Regenerated the complete root manifest and checksum inventory and reran the final publication-package verifier.

## v1.7.0 - final local package, remote tag not performed (2026-07-28)

- Phase3B fixed the current E002 lineage to the Phase2C official empty-cache
  run, verified 8/8 designated HTS67 substantive tables as byte-identical to
  the preserved historical substantive reference, and preserved the earlier
  non-byte-identical comparison unchanged under a non-current historical role.
- Added E001 fixed-seed CMB bootstrap replay for N025-N026.
- Added E002 two-layer posterior-attribution replay for N029-N035.
- Added official input locators and a 51-member hash manifest without redistributing chain bytes.
- Added verified portable replicas of historical intermediate inputs required by HTS66; the earlier non-byte-identical HTS67 numerical comparison is retained only as a non-current historical replay record.
- Preserved C001-C030, N001-N046, and V001 without scientific changes.
- Updated Table 1, reproducibility records, content policy, verifier, manifests, and release documentation.
- Repaired E002 so fresh-output verification reads newly generated HTS59-HTS67 outputs directly.
- Added the verified HTS67 compatibility cache view and dual historical/current stage checksum records.
- Added path-sanitized portable replicas for HTS59-HTS65 and the HTS66 correction input; the canonical Phase2C comparison now establishes byte identity only for the eight designated HTS67 substantive tables.
- Completed fresh E001 and E002 replay from newly empty work/output trees using hash-verified inputs.
- Phase2C completed official acquisition from a newly empty external cache in a network-enabled WSL environment: 51/51 selected members and E002 passed. The ORIGINAL archive used HTTP Range and was not fully materialized; its observed ETag differs from the recorded ETag and is retained as non-identity HTTP metadata.
- Restored the full 13-capability publication-package verifier and verified its final-package mode.
- Synchronized the manuscript Abstract, computational boundary, Results 3.5, Limitations, Data and Code Availability, and Table 1 with the Phase2C eight-table byte-identity boundary.
- Regenerated the complete root manifest and checksum inventory after adding the final DOCX and PDF.
- Left GitHub tag/Release, persistent-identifier, and Jxiv actions explicitly unperformed.

## v1.6.1 - manuscript plus version-fixed repository publication model

- Removed the obsolete Jxiv supplementary-ZIP publication model.
- Replaced Supplement locators with repository-relative public evidence paths for C001-C030.
- Added `PROVENANCE/REPRODUCTION_STATUS.tsv` to distinguish output traceability from re-execution.
- Added a bounded DESI BAO Gaussian-fit reproduction contract using fixed external inputs.
- Preserved C001-C030, N001-N046, V001, and all scientific values and status histories.
- Updated repository and manuscript metadata to v1.6.1 without rewriting v1.6.0 history.
- Applied final pre-tag consistency corrections: removed the manuscript page-break defect before Figure 2, synchronized the BAO Table 1 evidence-state wording, corrected the release checklist locator-metadata statement, clarified non-redistribution of the historical TDCOSMO governance utility, and updated repository structure/licensing text.


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
