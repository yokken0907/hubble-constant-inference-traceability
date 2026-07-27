Yoshimura (2026) - Public Traceability Archive, Version 1.5.5
=======================================================================

Purpose
-------
This archive accompanies "Dependency and Numerical Traceability in Public Hubble-Constant Inference." It contains publication-facing tables, figure-source data, English provenance registers, numerical-validation records, and selected author-generated analysis outputs. It is a repository-oriented traceability archive, not a second publication of the manuscript.

Version 1.5.5 revision
--------------------------
Stable NUMBER_ID values N001-N046 were added directly to TABLES/TABLE2_NUMERICAL_RESULTS.tsv. The ID mapping is documented in PROVENANCE/TABLE2_NUMBER_ID_VALIDATION.tsv. No scientific values, units, scopes, interpretations, or claim statuses were changed.

Source archive identity
-----------------------
FROZEN_CORE_SOURCE_ARCHIVE_FILENAME = Yoshimura_2026_Dependency_and_Numerical_Traceability_in_Public_Hubble_Constant_Inference_Data.zip
FROZEN_CORE_SOURCE_ARCHIVE_SHA256   = e7074403b3fc4ddce1b11c05696cc3735b1f39c52fc5cb0e71ce517ebb949bce
FROZEN_CORE_SOURCE_ARCHIVE_INCLUDED = NO

The hash above identifies the internal assembly source archive. It is not the hash of this repository ZIP.

Top-level structure
-------------------
TABLES/
  Machine-readable versions of the four principal manuscript tables and derived diagnostics.
FIGURE_SOURCE_DATA/
  Data used to construct the four principal figures.
PROVENANCE/
  Statement-to-evidence, numerical-validation, source/version, archived-output, path-mapping, and Table 2 ID-mapping records.
ANALYSIS_OUTPUTS/
  Selected author-generated summaries and audit records retained for numerical traceability.
tools/
  Dependency-free repository integrity and navigation utilities.

Reproducibility boundary
------------------------
The archive supports numerical traceability from manuscript statements and tables to specified author-generated outputs and identified public-source versions. It does not contain large third-party posterior archives, likelihood products, or raw observational releases. Except where the manuscript explicitly reports re-execution or a separately written check, the archive should not be interpreted as enabling full reconstruction from raw data or as independent validation of the original collaborations' pipelines.

Licensing
---------
Documentation, tables, data files, provenance registers, and audit records are CC BY 4.0 unless stated otherwise. Python source files under tools/ are MIT licensed. Third-party materials retain their original terms.

Publication metadata
--------------------
MANUSCRIPT_STATUS = PREPARED_FOR_JXIV_SUBMISSION
PERSISTENT_IDENTIFIER = NOT_ASSIGNED
REPOSITORY_PUBLIC_URL = https://github.com/yokken0907/hubble-constant-inference-traceability

Only actual public URLs and identifiers should be added after publication.
