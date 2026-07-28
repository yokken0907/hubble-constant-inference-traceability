# Release notes — v1.6.0 release candidate

## Purpose

Version 1.6.0 formally connects the later TDCOSMO second-implementation evidence to the public provenance system while preserving the published v1.5.5 history.

## Added

- `PROVENANCE/POST_SYNTHESIS_VALIDATION_REGISTER.tsv`
- `PROVENANCE/V001_EVIDENCE_PATHS.tsv`
- `PROVENANCE/V1_5_5_PRESERVATION_RECORD.tsv`
- `POST_SYNTHESIS_VALIDATION/tdcosmo_second_implementation/`

## Historical preservation

The original C026/C027 records are unchanged. Their `NOT_DONE` and HOLD states describe the 2026-07-24/25 historical stage before the later second implementation.

The later V001 record describes a subsequent workflow and ends at `COMPLETE_WITH_SCOPE`.

## Bounded result

- 13/13 structural comparisons passed.
- 39/39 q16/q50/q84 comparisons passed within the frozen project tolerance.
- 12/12 Table 6 rows matched at published precision.

## No scientific-value change

Table 2 and all `N001–N046` values, units, scopes, and identifiers are byte-for-byte unchanged from v1.5.5.

## No expanded scientific claim

The added evidence is not external independent replication and does not reproduce the original likelihood, sampler, convergence diagnostics, posterior weights, or posterior-generation pipeline.

## Public-release boundary

The `v1.6.0` tag and release URL must be recorded only after they actually exist. The existing `v1.5.5` tag and release must not be moved or replaced.
