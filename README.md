# Dependency and Numerical Traceability in Public Hubble-Constant Inference

[日本語版 README](README_JA.md)

This repository is the public scientific traceability archive associated with:

> **Dependency and Numerical Traceability in Public Hubble-Constant Inference**  
> *An Integrated Audit of the Local Distance Ladder, Supernova Processing, BAO, CMB, Posterior Geometry, and Other Distance Methods*  
> Keiji Yoshimura, Independent Researcher (2026)

The fixed scientific archive baseline is [GitHub Release v1.7.1](https://github.com/yokken0907/hubble-constant-inference-traceability/releases/tag/v1.7.1) (tag `v1.7.1`; commit `8ada39da3c712923b70bae0c060388180e0f3a82`). Later repository editions may correct reader-facing documentation or publication metadata without altering that fixed scientific baseline.

## Current repository state

```text
REPOSITORY_RELEASE = v1.7.3
SCIENTIFIC_ARCHIVE_BASELINE = v1.7.1
SCIENTIFIC_ARCHIVE_TAG = v1.7.1
SCIENTIFIC_ARCHIVE_COMMIT = 8ada39da3c712923b70bae0c060388180e0f3a82
ORIGINAL_STATEMENT_COUNT = 30
ORIGINAL_NUMBER_COUNT = 46
POST_SYNTHESIS_VALIDATIONS = 1
BOUNDED_REPLAY_RECORDS = 2
SCIENTIFIC_VALUES_CHANGED = NO
INDEPENDENT_EXPERT_REVIEW = PENDING
```

Version `v1.7.3` is the current reader-facing repository edition. Version `v1.7.1` remains the fixed scientific archive baseline. These versions have different functions and must not be treated as interchangeable. Version `v1.7.2` remains an unchanged historical metadata release.

## Claim boundary

This repository does **not** claim:

- resolution of the Hubble tension;
- identification of a unique cause or uniquely justified correction;
- a new independent measurement of the Hubble constant;
- validation of the originating collaborations' complete pipelines;
- external independent replication; or
- evidence for new physics.

Its purpose is narrower: to make registered statements, numerical values, source versions, author-generated outputs, bounded validation and replay records, and stated limitations inspectable and cross-referenced.

## Version 1.7.3 scope

Version `v1.7.3` is a reader-facing disclosure and publication-metadata normalization. It:

- removes the special AI-centered report branding introduced in `v1.7.2` from current landing and citation metadata;
- restores the associated study's standard scientific title and subtitle in reader-facing records;
- retains explicit disclosure that generative AI was used extensively, while also stating the human author's actual research-direction, claim-control, correction, and release responsibilities;
- keeps publication metadata platform-neutral until an actual public report identifier is issued;
- distinguishes the current repository edition from the fixed scientific archive baseline;
- regenerates the root manifest and checksum closure; and
- introduces no new scientific claim.

The change does **not** reclassify the work as human-only, does not conceal substantive AI assistance, and does not alter the scientific analysis. It corrects the presentation of the human-AI division of labor so that neither side is overstated or understated.

The following scientific records remain unchanged:

- statements `C001`-`C030`;
- principal numerical results `N001`-`N046`;
- post-synthesis validation `V001`;
- bounded replay records `E001` and `E002`;
- numerical values, units, tolerances, evidence hashes, classifications, and claim boundaries.

## Fixed scientific archive baseline

```text
RELEASE = v1.7.1
TAG = v1.7.1
COMMIT = 8ada39da3c712923b70bae0c060388180e0f3a82
URL = https://github.com/yokken0907/hubble-constant-inference-traceability/releases/tag/v1.7.1
```

The existing `v1.7.1` tag and Release are historical scientific records and must not be moved, replaced, or regenerated. The `v1.7.3` documentation update does not rewrite the scientific archive history. The `v1.7.2` metadata release also remains historical and unchanged.

## Source archive identity

```text
FROZEN_CORE_SOURCE_ARCHIVE_FILENAME = Yoshimura_2026_Dependency_and_Numerical_Traceability_in_Public_Hubble_Constant_Inference_Data.zip
FROZEN_CORE_SOURCE_ARCHIVE_SHA256 = e7074403b3fc4ddce1b11c05696cc3735b1f39c52fc5cb0e71ce517ebb949bce
FROZEN_CORE_SOURCE_ARCHIVE_INCLUDED = NO
```

This hash identifies the internal source archive used to assemble the original public core; it is not the hash of a GitHub-generated archive or of the current repository ZIP. See [`SOURCE_ARCHIVE_RECORD.md`](SOURCE_ARCHIVE_RECORD.md).

## Start here

| Question | File |
|---|---|
| What is this archive and how should it be read? | [`TRACEABILITY_ARCHIVE_DESCRIPTION.pdf`](TRACEABILITY_ARCHIVE_DESCRIPTION.pdf) |
| Which statement is supported by which evidence? | [`PROVENANCE/STATEMENT_TO_EVIDENCE_REGISTER.tsv`](PROVENANCE/STATEMENT_TO_EVIDENCE_REGISTER.tsv) |
| Where do the 46 principal numerical results come from? | [`PROVENANCE/PRINCIPAL_NUMERICAL_RESULTS_VALIDATION.tsv`](PROVENANCE/PRINCIPAL_NUMERICAL_RESULTS_VALIDATION.tsv) |
| How do Table 2 rows map to `N001`-`N046`? | [`PROVENANCE/TABLE2_NUMBER_ID_VALIDATION.tsv`](PROVENANCE/TABLE2_NUMBER_ID_VALIDATION.tsv) |
| Which public source and version was used? | [`PROVENANCE/SOURCE_AND_VERSION_RECORDS.tsv`](PROVENANCE/SOURCE_AND_VERSION_RECORDS.tsv) |
| Which bounded validation followed the original synthesis? | [`PROVENANCE/POST_SYNTHESIS_VALIDATION_REGISTER.tsv`](PROVENANCE/POST_SYNTHESIS_VALIDATION_REGISTER.tsv) |
| Which calculations were replayed? | [`PROVENANCE/REEXECUTION_EVIDENCE_REGISTER.tsv`](PROVENANCE/REEXECUTION_EVIDENCE_REGISTER.tsv) |
| What is the status of each analysis route? | [`PROVENANCE/REPRODUCTION_STATUS.tsv`](PROVENANCE/REPRODUCTION_STATUS.tsv) |
| What can and cannot be reproduced? | [`REPRODUCIBILITY.md`](REPRODUCIBILITY.md) |
| What is the current public-release state? | [`RELEASE_STATUS.md`](RELEASE_STATUS.md) |
| What are the current file hashes? | [`MANIFEST.tsv`](MANIFEST.tsv) and [`SHA256SUMS.txt`](SHA256SUMS.txt) |

## Quick verification

Python 3.9 or later is sufficient for the repository integrity verifier; no third-party Python package is required.

```bash
python tools/verify_publication_package.py --final-package
```

Trace a registered record:

```bash
python tools/trace_record.py C026
python tools/trace_record.py N001
python tools/trace_record.py E001
python tools/trace_record.py E002
python tools/trace_record.py R008
python tools/trace_record.py R012
python tools/trace_record.py S001
python tools/trace_record.py V001
```

## Structure

```text
TABLES/                    machine-readable public tables
FIGURE_SOURCE_DATA/        source data for the principal figures
PROVENANCE/                statement, number, source, validation, path, and hash registers
ANALYSIS_OUTPUTS/          selected author-generated historical summaries and audit records
POST_SYNTHESIS_VALIDATION/ bounded validation evidence integrated after the original audit
REPRODUCTION/              bounded re-execution contracts, code, manifests, and expected outputs
TRACEABILITY_ARCHIVE_DESCRIPTION.pdf  bilingual archive guide and interpretation boundary
tools/                     navigation and integrity utilities
.github/FUNDING.yml        GitHub Sponsors configuration
MANIFEST.tsv               release path, byte-size, category, and SHA-256 inventory
SHA256SUMS.txt              checksums for every release file except the checksum file itself
```

## Evidence and reproducibility boundary

The archive distinguishes:

1. file identity and provenance;
2. output-level numerical traceability;
3. re-execution from stated inputs and an identified implementation;
4. robustness within a shared source;
5. descriptive agreement across source summaries;
6. project-internal implementation diversity; and
7. causal attribution.

Establishing one level does not automatically establish the next. `V001`, `E001`, and `E002` are bounded project-internal validation or replay records. They do not reconstruct the originating likelihoods, samplers, burn-in, thinning, convergence assessment, posterior weights, log probabilities, or posterior-generation environments, and they are not external independent replication.

## AI assistance and human accountability

Generative AI was used extensively as a research tool. OpenAI ChatGPT assisted with organizing public materials, research framing, candidate methodology, code drafting, cross-source synthesis, numerical interpretation, evidence mapping, documentation, and manuscript preparation. OpenAI Codex supported code-generation, repository inspection, metadata maintenance, and packaging-related tasks.

AI output itself was not treated as evidence; scientific claims are tied to cited public sources and frozen project records. The human author selected the research subject and questions, approved scope and claim boundaries, directed the workflow, operated the computational process, requested reruns and corrections, made stopping and release decisions, maintained provenance, and retains responsibility for correcting or withdrawing public claims shown to be unsupported. This work has not been independently certified by a domain expert.

See [`AI_DISCLOSURE.md`](AI_DISCLOSURE.md) for the detailed role statement.

## Citation

Use [`CITATION.cff`](CITATION.cff) for repository metadata. The fixed scientific traceability archive is [GitHub Release v1.7.1](https://github.com/yokken0907/hubble-constant-inference-traceability/releases/tag/v1.7.1). A manuscript/preprint URL, DOI, or other persistent identifier should be added only in a later repository version after the identifier actually exists.

## License

- Author-generated prose, tables, figures, and documentation: [`LICENSE`](LICENSE)
- Code under `tools/`: [`tools/LICENSE`](tools/LICENSE)
- Third-party materials remain subject to their original terms.
