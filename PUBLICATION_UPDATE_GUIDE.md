# Publication metadata update guide

This release is prepared before the public repository URL, release URL, Jxiv URL, and persistent identifiers are finalized. Do not insert provisional identifiers.

## After the repository becomes public

1. Confirm that the public repository URL is accessible from a logged-out browser.
2. Record the actual public repository URL in `README.md`, `README_JA.md`, and `CITATION.cff`.
3. Before final Jxiv submission, add the confirmed repository URL to the manuscript's appropriate Data Availability, Code Availability, or equivalent section.
4. If a release URL or persistent identifier has been assigned, record only the identifier that actually exists.
5. Regenerate `MANIFEST.tsv` and `SHA256SUMS.txt` after all metadata updates.
6. Re-run the repository verification scripts and confirm that all integrity checks pass.

## After the Jxiv record becomes public

1. Record the actual Jxiv URL, DOI, or other identifier exactly as assigned.
2. Update the manuscript citation metadata in `CITATION.cff` using the public Jxiv record.
3. Update `README.md` and `README_JA.md` with the public manuscript citation.
4. Do not describe the manuscript as peer reviewed, accepted by a journal, or independently validated unless that status is separately established.
5. Regenerate `MANIFEST.tsv` and `SHA256SUMS.txt` after the metadata update.
6. Re-run the repository verification scripts and confirm that all integrity checks pass.

## Optional later archival identifier

If a DOI or other persistent identifier is assigned to a versioned repository or data release after the Jxiv publication boundary has been safely handled, record only the identifier actually issued. Do not invent or reserve a placeholder DOI.
