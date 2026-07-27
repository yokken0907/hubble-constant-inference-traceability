# Release checklist

## v1.6.0 final candidate (package-build record)

- [x] Base package verified as v1.5.5 before integration
- [x] Existing v1.5.5 tag, release, and history left untouched
- [x] Original statement count remains 30
- [x] Original numerical-result count remains 46
- [x] `TABLES/TABLE2_NUMERICAL_RESULTS.tsv` is byte-for-byte unchanged from v1.5.5
- [x] `PROVENANCE/STATEMENT_TO_EVIDENCE_REGISTER.tsv` is byte-for-byte unchanged from v1.5.5
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
- [x] Privacy, credential, absolute-personal-path, and third-party-byte scan passes
- [x] Package-build state records that the `v1.6.0` tag and Release were not yet assigned
- [ ] Post-build repository action: create the `v1.6.0` tag and Release after independent final review
- [ ] Post-build metadata action: record the actual v1.6.0 release URL only after it exists
- [ ] Post-publication metadata action: add Jxiv metadata only after the actual Jxiv record becomes public

Unchecked items are external actions outside this immutable package-build record and must not be completed provisionally.
