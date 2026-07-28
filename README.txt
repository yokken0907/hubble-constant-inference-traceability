PACKAGE_VERSION = 1.7.0
TARGET_PUBLIC_RELEASE = v1.7.0
PUBLIC_TAG_STATUS = NOT_CREATED_OR_INDEPENDENTLY_VERIFIED
E001_FRESH_REPLAY = PASS
E002_FRESH_REPLAY = PASS_FROM_OFFICIAL_EMPTY_CACHE
OFFICIAL_FETCH_EMPTY_CACHE_STATUS = PASS_WITH_SCOPE_RANGE_SELECTED_MEMBER_IDENTITY
LOCAL_FINAL_PACKAGE = PASS
REMOTE_TAG_ACTION = NOT_PERFORMED
PUBLICATION_MODEL = MANUSCRIPT_PLUS_VERSION_FIXED_GITHUB_REPOSITORY
JXIV_SUPPLEMENTARY_ZIP = NOT_USED
FULL_RAW_DATA_TO_POSTERIOR_REPRODUCTION = NOT_CLAIMED

Yoshimura (2026) - Public Traceability Archive, Version 1.7.0
=======================================================================

Purpose
-------
This archive accompanies "Dependency and Numerical Traceability in Public Hubble-Constant Inference." It contains publication-facing tables, figure-source data, provenance registers, numerical-validation records, selected author-generated analysis outputs, and one later bounded post-synthesis validation record.

Version 1.7.0
-------------
Version 1.7.0 preserves the V001 evidence introduced in v1.6.0 and adopts the manuscript-plus-version-fixed-repository publication model. It adds repository-relative evidence locations, reproduction-status records, and a DESI BAO fixed-external-input reproduction contract.

The result is recorded separately as V001:
- 13/13 structural comparisons passed;
- 39/39 q16/q50/q84 comparisons passed within the frozen tolerance;
- 12/12 Table 6 rows matched at published precision;
- final status COMPLETE_WITH_SCOPE.

The original 30 statements C001-C030 and 46 principal numerical results N001-N046 are unchanged. Historical C026/C027 records stating NOT_DONE and HOLD remain valid for their earlier stage and are not overwritten.

Version relationship
--------------------
BASE_PUBLIC_VERSION = 1.5.5
PACKAGE_BUILD_STATUS         = FINAL_ASSEMBLED_UNTAGGED_V1.7.0
V1_5_5_HISTORY_PRESERVED = YES

The v1.5.5 tag and release must not be repointed, replaced, or rewritten.

Post-synthesis evidence
-----------------------
POST_SYNTHESIS_VALIDATION/tdcosmo_second_implementation/ contains the selected public evidence. Third-party HDF5 files and the source paper PDF are not redistributed.

The implementation-diversity check does not reproduce the original likelihood, sampler, convergence diagnostics, posterior weights, or posterior-generation pipeline and is not external independent replication.

Verification
------------
Run:

python tools/verify_publication_package.py --final-package
python tools/trace_record.py V001

Publication metadata
--------------------
REPOSITORY_RELEASE_FILES     = 483 files
HASHED_RELEASE_FILES         = 482 / 482 VERIFIED
MANUSCRIPT_STATUS = FINAL_LOCAL_PACKAGE; REMOTE_PUBLICATION_NOT_PERFORMED
PERSISTENT_IDENTIFIER = NOT_ASSIGNED
REPOSITORY_PUBLIC_URL = https://github.com/yokken0907/hubble-constant-inference-traceability

At package-build time, the v1.7.0 tag and release had not been assigned. If identifiers are added later, record only actual public tags, release URLs, Jxiv records, and persistent identifiers.

Licensing
---------
Documentation, tables, data files, provenance registers, and audit records are CC BY 4.0 unless stated otherwise. Python source files under tools/ and the designated V001 implementation are MIT licensed. Third-party materials retain their original terms.


## Version 1.7.0 replay extension

Version 1.7.0 adds two project-internal replay records without changing C001-C030, N001-N046, or V001: `E001` for the fixed-seed CMB bootstrap (N025-N026) and `E002` for the two-layer posterior-attribution workflow (N029-N035). Third-party posterior chain bytes are not redistributed. See `PROVENANCE/REEXECUTION_EVIDENCE_REGISTER.tsv` and the two new `REPRODUCTION/` capsules.
HTS67_PHASE2C_CANONICAL_RUN = PASS
HTS67_SUBSTANTIVE_TABLE_BYTE_IDENTITY = 8/8 PASS
EARLIER_REPLAY_PROVENANCE_SEPARATED = PASS
GLOBAL_HISTORY_SOURCE_REGISTER = PASS
OFFICIAL_FETCH_EMPTY_CACHE = PASS_WITH_SCOPE_RANGE_SELECTED_MEMBER_IDENTITY
LOCAL_PUBLICATION_PACKAGE_READY = PASS
REMOTE_PUBLICATION_ACTIONS = NOT_PERFORMED
