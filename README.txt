Yoshimura (2026) - Public Traceability Archive, Version 1.6.0
=======================================================================

Purpose
-------
This archive accompanies "Dependency and Numerical Traceability in Public Hubble-Constant Inference." It contains publication-facing tables, figure-source data, provenance registers, numerical-validation records, selected author-generated analysis outputs, and one later bounded post-synthesis validation record.

Version 1.6.0
-------------
Version 1.6.0 adds the public evidence chain for a later project-internal second-implementation check of released TDCOSMO HDF5 sample summaries.

The result is recorded separately as V001:
- 13/13 structural comparisons passed;
- 39/39 q16/q50/q84 comparisons passed within the frozen tolerance;
- 12/12 Table 6 rows matched at published precision;
- final status COMPLETE_WITH_SCOPE.

The original 30 statements C001-C030 and 46 principal numerical results N001-N046 are unchanged. Historical C026/C027 records stating NOT_DONE and HOLD remain valid for their earlier stage and are not overwritten.

Version relationship
--------------------
BASE_PUBLIC_VERSION = 1.5.5
PACKAGE_BUILD_STATUS = FINAL_CANDIDATE_FOR_V1.6.0
V1_5_5_HISTORY_PRESERVED = YES
TAG_V1_6_0_STATUS_AT_PACKAGE_BUILD = NOT_ASSIGNED

The v1.5.5 tag and release must not be repointed, replaced, or rewritten.

Post-synthesis evidence
-----------------------
POST_SYNTHESIS_VALIDATION/tdcosmo_second_implementation/ contains the selected public evidence. Third-party HDF5 files and the source paper PDF are not redistributed.

The implementation-diversity check does not reproduce the original likelihood, sampler, convergence diagnostics, posterior weights, or posterior-generation pipeline and is not external independent replication.

Verification
------------
Run:

python tools/verify_publication_package.py
python tools/trace_record.py V001

Publication metadata
--------------------
REPOSITORY_RELEASE_FILES = 155
HASHED_RELEASE_FILES = 154 / 154 VERIFIED
MANUSCRIPT_STATUS = PREPARED_FOR_JXIV_SUBMISSION
PERSISTENT_IDENTIFIER = NOT_ASSIGNED
REPOSITORY_PUBLIC_URL = https://github.com/yokken0907/hubble-constant-inference-traceability

At package-build time, the v1.6.0 tag and release had not been assigned. If identifiers are added later, record only actual public tags, release URLs, Jxiv records, and persistent identifiers.

Licensing
---------
Documentation, tables, data files, provenance registers, and audit records are CC BY 4.0 unless stated otherwise. Python source files under tools/ and the designated V001 implementation are MIT licensed. Third-party materials retain their original terms.
