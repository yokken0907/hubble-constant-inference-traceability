# Release checklist

## v1.7.0 final local package (package-build record)

- [x] Base package verified as v1.5.5 before integration
- [x] Existing v1.5.5 tag, release, and history left untouched
- [x] Original statement count remains 30
- [x] Original numerical-result count remains 46
- [x] `TABLES/TABLE2_NUMERICAL_RESULTS.tsv` is byte-for-byte unchanged from v1.5.5
- [x] Scientific statement content is unchanged; locator/source-path metadata were updated in v1.7.0
- [x] Historical C026/C027 `NOT_DONE` and HOLD records remain unchanged
- [x] Later V001 `COMPLETE_WITH_SCOPE` record added separately
- [x] Second-implementation code identified and SHA-256 verified
- [x] 13-input source manifest included without redistributing HDF5 files
- [x] Method, tolerance, source, and stopping-rule freeze documented
- [x] 13/13 structural, 39/39 quantile, and 12/12 Table 6 results connected to public evidence paths
- [x] Project-internal implementation is not described as external independent replication
- [x] No original likelihood or posterior-generation reconstruction claimed
- [x] No new causal, correction, new-physics, or Hubble-tension-resolution claim added
- [x] `MANIFEST.tsv` and `SHA256SUMS.txt` regenerated
- [x] Local V001 `SHA256SUMS.txt` regenerated
- [x] Repository verification scripts pass
- [x] Credential and third-party-byte scan passes; no secret markers were found. Absolute execution paths occur only inside preserved official-fetch evidence records and are not active configuration.
- [x] Package-build state records that the `v1.7.0` tag and Release were not yet assigned
- [x] Manuscript current-state wording synchronized to the successful Phase2C acquisition boundary
- [x] Final DOCX and PDF included under `MANUSCRIPT/` and visually inspected
- [x] Complete root `MANIFEST.tsv` and `SHA256SUMS.txt` regenerated after document synchronization
- [x] `python tools/verify_publication_package.py --final-package` passes all 13 capability gates
- [ ] Post-build repository action: create the `v1.7.0` tag and Release after independent final review
- [ ] Post-build metadata action: record the actual v1.7.0 release URL only after it exists
- [ ] Post-publication metadata action: add Jxiv metadata only after the actual Jxiv record becomes public

Unchecked items are external actions outside this immutable package-build record and must not be completed provisionally.

- [ ] Confirm no Jxiv supplementary ZIP is attached
- [ ] Confirm v1.7.0 tag points to the final verified commit and v1.6.0 is unchanged
- [x] Confirm `PROVENANCE/REPRODUCTION_STATUS.tsv` and DESI reproduction contract are present

- [x] E001 clean replay reproduced N025-N026 with seed 10199 and 1,000 draws.
- [x] E002 fresh portable replay reproduced N029-N035 from the newly generated output directory; `E002_FRESH_OUTPUT_COMPARISON.tsv` is PASS.
- [x] Failed HTS66 HOLD ZIP excluded from all canonical roles.
- [x] Third-party posterior chain bytes excluded; 51-member hash manifest included.
- [x] Phase2C official acquisition from a newly empty external cache completed in a network-enabled WSL environment; 51/51 selected members and E002 passed.
- [ ] Create and independently verify the public v1.7.0 tag and Release from the final verified package.
## Final provenance and official-fetch gate

- [x] Global `REPRODUCTION/posterior_attribution/HISTORY_SOURCE_REGISTER.tsv` regenerated from all stage-local registers; current hashes and row set verified.
- [x] Phase2C official empty-cache HTS67 result ZIP fixed as the sole current E002 acceptance lineage.
- [x] `HTS67_HISTORICAL_VS_FRESH_COMPARISON.tsv` is generated from the actual Phase2C ZIP and records 8/8 designated substantive tables as byte-identical.
- [x] Earlier non-byte-identical comparison preserved unchanged under `historical_earlier_replay/` and excluded from the current acceptance role.
- [x] `OFFICIAL_FETCH_EMPTY_CACHE = PASS_WITH_SCOPE`: ORIGINAL used official HTTP Range with 40/40 selected-member hashes; FIXED full archive SHA-256 and 11/11 selected-member hashes passed; full ORIGINAL archive SHA-256 was not materialized or claimed.
- [x] Local document synchronization and final package regeneration completed; the acquisition gate passed with the recorded scope.
- [ ] Set or cite the remote tag only after confirming that it points to the verified final commit.
