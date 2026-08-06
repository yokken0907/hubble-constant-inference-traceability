# Repository tools

The scripts in this directory require Python 3.9 or later and no third-party packages.

```bash
python tools/verify_publication_package.py
python tools/trace_record.py C026
python tools/trace_record.py N001
python tools/trace_record.py S001
python tools/trace_record.py V001
```

`verify_publication_package.py` checks:

- repository-wide manifest and SHA-256 coverage;
- the local V001 evidence checksum inventory;
- the unchanged 30-statement historical register;
- the unchanged `N001–N046` mapping and numerical-validation statuses;
- the v1.5.5 preservation record;
- V001 evidence registration;
- the fixed second-implementation code hash;
- 13/13 structural, 39/39 quantile, and 12/12 Table 6 validation records.

The integrity verifier validates recorded files and statuses. It does not rerun scientific analyses or recalculate posterior quantiles.
