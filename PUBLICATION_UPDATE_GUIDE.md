# Publication metadata update guide

The public repository URL is finalized and recorded as:

```text
REPOSITORY_PUBLIC_URL = https://github.com/yokken0907/hubble-constant-inference-traceability
```

The v1.6.0 package is a release candidate. No `v1.6.0` tag URL, v1.6.0 release URL, Jxiv URL, Jxiv DOI, or other persistent identifier is asserted before it exists.

The existing v1.5.5 tag and release are historical records and must not be repointed, replaced, or rewritten.

## Before publishing v1.6.0

1. Confirm that the v1.6.0 candidate ZIP passes all integrity checks.
2. Confirm that the v1.5.5 tag still points to its original commit.
3. Create a new `v1.6.0` tag targeting the final v1.6.0 commit.
4. Publish a new v1.6.0 Release without replacing v1.5.5 assets.
5. Record the actual v1.6.0 release URL only after it exists.
6. Regenerate repository metadata and hashes if any tracked file is changed after this candidate package.

## Before final Jxiv submission

1. Confirm once more that the public repository URL is accessible.
2. Add the confirmed repository URL to the manuscript's Data and Code Availability section.
3. If the v1.6.0 tag or release has actually been published, record its real URL.
4. Do not insert provisional identifiers.
5. Re-run all integrity checks after any metadata update.

## After the Jxiv record becomes public

1. Record the actual Jxiv URL, DOI, or other identifier exactly as assigned.
2. Update `CITATION.cff` using the public Jxiv record.
3. Update `README.md` and `README_JA.md` with the public manuscript citation.
4. Do not describe the manuscript as peer reviewed, journal accepted, or independently validated unless separately established.
5. Regenerate `MANIFEST.tsv` and `SHA256SUMS.txt`.
6. Re-run all verification scripts.
