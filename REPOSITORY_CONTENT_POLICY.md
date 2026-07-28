# Repository Content Policy

This repository is intentionally selective.

## Included

- publication tables and figure-source data;
- the statement-to-evidence and principal-number registers;
- public source and version records;
- selected author-generated outputs needed to inspect manuscript claims;
- documented corrections relevant to the current canonical interpretation;
- integrity metadata and small navigation utilities.

## Excluded

- the full internal development archive;
- routine intermediate HTV/HTS packages;
- superseded packages that do not affect the publication claim boundary;
- duplicate caches;
- large third-party data or posterior files;
- manuscript submission files and any Jxiv supplementary ZIP; the version-fixed repository is the associated public traceability archive; and
- unrelated later-phase, exploratory, or subsequent research branches.

An item should be added only when it materially improves the ability to trace, verify, interpret, or correct a claim in the associated manuscript.

## v1.7.0 posterior-export fetch policy

Third-party posterior chain bytes are not included in the repository or release assets. The E002 capsule retrieves official archives, verifies archive identity where available, and verifies all 51 selected members by byte size and SHA-256. A newer or differently hashed release must not be substituted for the recorded historical input.
