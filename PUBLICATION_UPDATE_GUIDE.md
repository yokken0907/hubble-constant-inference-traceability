# Publication Metadata Update Guide

This guide governs later publication-metadata updates without rewriting the fixed scientific archive history.

## Current fixed scientific archive

The associated AI-led research report (version v1.7.1-AIRR2) cites:

```text
RELEASE = v1.7.1
TAG = v1.7.1
COMMIT = 8ada39da3c712923b70bae0c060388180e0f3a82
URL = https://github.com/yokken0907/hubble-constant-inference-traceability/releases/tag/v1.7.1
```

The release, tag, and commit above are immutable historical references for this project. Later metadata versions must not move or replace them.

## Rules for later publication metadata

1. Record only URLs, DOIs, or identifiers that actually exist.
2. Do not pre-populate a planned publication destination.
3. Add new bibliographic metadata in a new repository version.
4. Preserve the fixed `v1.7.1` scientific archive citation used by the report.
5. Do not alter `C001`-`C030`, `N001`-`N046`, `V001`, `E001`, `E002`, scientific values, tolerances, evidence hashes, classifications, or claim boundaries for a metadata-only update.
6. Keep the public-report model platform-neutral.

## After a public report record is assigned

1. Verify that the public record resolves without authentication.
2. Record the exact title, version, URL, date, and identifier as issued.
3. Update `README.md`, `README_JA.md`, `CITATION.cff`, and `RELEASE_STATUS.md` in a new version.
4. State that the report continues to cite fixed scientific archive Release `v1.7.1` unless the report itself is scientifically revised and explicitly cites another fixed archive.
5. Regenerate integrity metadata and rerun the final-package verifier.

## Version and integrity procedure

1. Start from the current default branch.
2. Make only the intended reader-facing metadata changes.
3. Review the changed-file list and confirm that all scientific files remain byte-identical.
4. Run:

   ```bash
   python tools/finalize_publication_package.py
   python tools/verify_publication_package.py --final-package
   ```

5. Confirm that `MANIFEST.tsv`, `SHA256SUMS.txt`, version fields, and release notes agree.
6. Create a new tag and Release only from the verified commit.
7. Verify again that tag `v1.7.1` still points to `8ada39da3c712923b70bae0c060388180e0f3a82`.

## Prohibited history rewrites

- Do not force-move or recreate the `v1.7.1` tag.
- Do not replace the `v1.7.1` Release as a way of updating metadata.
- Do not insert an unassigned URL, DOI, or identifier.
- Do not rewrite historical changelog or release-note entries to look current.
- Do not describe project-internal validation as external independent replication.
- Do not strengthen scientific claims through a documentation-only release.
