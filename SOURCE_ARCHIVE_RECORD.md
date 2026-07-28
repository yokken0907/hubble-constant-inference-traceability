# Frozen core source archive record

The following hash identifies the internal source archive used to assemble the original frozen public core from which this repository release was prepared.

```text
FROZEN_CORE_SOURCE_ARCHIVE_FILENAME = Yoshimura_2026_Dependency_and_Numerical_Traceability_in_Public_Hubble_Constant_Inference_Data.zip
FROZEN_CORE_SOURCE_ARCHIVE_SHA256   = e7074403b3fc4ddce1b11c05696cc3735b1f39c52fc5cb0e71ce517ebb949bce
FROZEN_CORE_SOURCE_ARCHIVE_INCLUDED = NO
```

The source archive itself is not included in this repository. Its SHA-256 is retained as an assembly-provenance identifier and must not be confused with the hash of the current repository ZIP or a future GitHub release asset.

Version 1.5.5 adds stable `NUMBER_ID` values directly to `TABLES/TABLE2_NUMERICAL_RESULTS.tsv` and updates publication metadata and licensing boundaries. It does not change the scientific values, units, scopes, claim statuses, or evidence interpretations inherited from the source archive.

The V001 post-synthesis evidence added in version 1.6.0 was assembled from separately preserved TDCOSMO validation packages and is not covered by the frozen-core source-archive hash above.

## v1.6.1 first-season re-audit

The complete two-part `1st season.zip` archive was recombined and checked before this revision. The combined SHA-256 was `2fc5069d3f64b28657de6fb7e7f6a9082621bc22db0d09b14390839f751937b5`; the outer archive and all 364 nested ZIP files passed CRC testing. Of 442 adjacent SHA-256 sidecars, 440 matched. Two historical mismatches were confined to a cache-index package and a non-canonical `HTV102_A` sidecar and are not used by the public evidence register. The DESI mean and covariance hashes used by the v1.6.1 reproduction contract were found consistently in the preserved HTV05 lineage.
