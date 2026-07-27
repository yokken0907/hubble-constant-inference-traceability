# Release checklist

## Public repository and pre-Jxiv submission

- [x] Repository URL confirmed from a logged-out browser
- [x] Public repository URL recorded in `README.md`, `README_JA.md`, `README.txt`, and `CITATION.cff`
- [x] GitHub Sponsors configuration stored at `.github/FUNDING.yml`
- [x] Version number matches `README.md`, `README_JA.md`, `README.txt`, `VERSION`, and `CITATION.cff`
- [x] `SHA256SUMS.txt` regenerated after the final repository-metadata modification
- [x] `MANIFEST.tsv` regenerated after the final repository-metadata modification
- [x] All 46 `NUMBER_ID` values are present in Table 2
- [x] No duplicate or missing `NUMBER_ID` values
- [x] All claim and evidence paths resolve within their declared inclusion boundary
- [x] No private email, API key, credential, or absolute personal path detected in the public release files
- [ ] Confirm that the final manuscript includes the public repository URL before Jxiv submission
- [ ] Create and cite a fixed Git tag or release if one is used
- [ ] Add Jxiv metadata only after the actual Jxiv record becomes public

Unchecked items require an action outside this repository package and must not be completed provisionally.
