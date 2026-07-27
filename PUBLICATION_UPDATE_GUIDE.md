# Publication metadata update guide

The public repository URL is finalized and recorded as:

```text
REPOSITORY_PUBLIC_URL = https://github.com/yokken0907/hubble-constant-inference-traceability
```

No Jxiv URL, Jxiv DOI, release URL, or other persistent identifier is assigned at this stage. Do not insert provisional identifiers.

## Before final Jxiv submission

1. Confirm once more that the public repository URL is accessible from a logged-out browser.
2. Add the confirmed repository URL to the manuscript's appropriate Data Availability, Code Availability, or equivalent section.
3. If a Git tag, release URL, or persistent identifier has actually been assigned, record only the identifier that exists.
4. Regenerate `MANIFEST.tsv` and `SHA256SUMS.txt` after any repository metadata update.
5. Re-run the repository verification scripts and confirm that all integrity checks pass.

## After the Jxiv record becomes public

1. Record the actual Jxiv URL, DOI, or other identifier exactly as assigned.
2. Update the manuscript citation metadata in `CITATION.cff` using the public Jxiv record.
3. Update `README.md` and `README_JA.md` with the public manuscript citation.
4. Do not describe the manuscript as peer reviewed, accepted by a journal, or independently validated unless that status is separately established.
5. Regenerate `MANIFEST.tsv` and `SHA256SUMS.txt` after the metadata update.
6. Re-run the repository verification scripts and confirm that all integrity checks pass.

## Optional later archival identifier

If a DOI or other persistent identifier is assigned to a versioned repository or data release after the Jxiv publication boundary has been safely handled, record only the identifier actually issued. Do not invent or reserve a placeholder DOI.
