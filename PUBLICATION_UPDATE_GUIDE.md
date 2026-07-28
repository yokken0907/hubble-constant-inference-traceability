# Publication metadata update guide

The public repository URL is finalized and recorded as:

```text
REPOSITORY_PUBLIC_URL = https://github.com/yokken0907/hubble-constant-inference-traceability
```

The v1.7.0 package is assembled and verified locally. No `v1.7.0` tag URL,
v1.7.0 release URL, Jxiv URL, Jxiv DOI, or other persistent identifier is
asserted before it exists.

The existing v1.5.5 tag and release are historical records and must not be repointed, replaced, or rewritten.

## Before publishing v1.7.0

1. Confirm that `python tools/verify_publication_package.py --final-package`
   passes all 13 capability gates in the exact tree to be published.
2. Confirm that the v1.5.5 tag still points to its original commit.
3. Confirm that any existing v1.6.0 tag remains unchanged.
4. Create a new `v1.7.0` tag targeting the final verified v1.7.0 commit.
5. Publish a new v1.7.0 Release without replacing historical assets.
6. Record the actual v1.7.0 release URL only after it exists.
7. If any tracked file changes, regenerate `MANIFEST.tsv` and
   `SHA256SUMS.txt`, then repeat final-package verification.

## Before final Jxiv submission

1. Confirm once more that the public repository URL is accessible.
2. Add the confirmed repository URL to the manuscript's Data and Code Availability section.
3. If the v1.7.0 tag or release has actually been published, record its real URL.
4. Do not insert provisional identifiers.
5. Re-run all integrity checks after any metadata update.

## After the Jxiv record becomes public

1. Record the actual Jxiv URL, DOI, or other identifier exactly as assigned.
2. Update `CITATION.cff` using the public Jxiv record.
3. Update `README.md` and `README_JA.md` with the public manuscript citation.
4. Do not describe the manuscript as peer reviewed, journal accepted, or independently validated unless separately established.
5. Regenerate `MANIFEST.tsv` and `SHA256SUMS.txt`.
6. Re-run all verification scripts.

## v1.7.0 Jxiv submission model

Submit the manuscript without a supplementary ZIP. Cite the public repository
and the version-fixed v1.7.0 snapshot only after the tag resolves publicly. The
repository is the sole associated traceability archive; the local release ZIP
is a transport copy of the same verified tree.
