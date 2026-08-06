REPOSITORY_RELEASE = v1.7.2
SCIENTIFIC_ARCHIVE_BASELINE = v1.7.1
SCIENTIFIC_ARCHIVE_TAG = v1.7.1
SCIENTIFIC_ARCHIVE_COMMIT = 8ada39da3c712923b70bae0c060388180e0f3a82
SCIENTIFIC_ARCHIVE_RELEASE_URL = https://github.com/yokken0907/hubble-constant-inference-traceability/releases/tag/v1.7.1
REPOSITORY_PUBLIC_URL = https://github.com/yokken0907/hubble-constant-inference-traceability
REPORT_EDITION = v1.7.1-AIRR2
REPORT_PUBLIC_IDENTIFIER = NOT_ASSIGNED
ORIGINAL_STATEMENT_COUNT = 30
ORIGINAL_NUMBER_COUNT = 46
POST_SYNTHESIS_VALIDATIONS = 1
BOUNDED_REPLAY_RECORDS = 2
SCIENTIFIC_VALUES_CHANGED = NO
INDEPENDENT_EXPERT_REVIEW = PENDING
LOCAL_PUBLICATION_PACKAGE_READY = PASS

TITLE = Dependency and Numerical Traceability in Public Hubble-Constant Inference: An AI-Led Public-Resource Research Report
SUBTITLE = An Integrated Audit of the Local Distance Ladder, Supernova Processing, BAO, CMB, Posterior Geometry, and Other Distance Methods

PURPOSE
Public scientific traceability archive for statement-to-evidence mapping,
numerical validation, source/version provenance, bounded validation, and
bounded replay records associated with the AI-led public-resource report.

FIXED SCIENTIFIC ARCHIVE
The associated report cites GitHub Release v1.7.1, tag v1.7.1, commit
8ada39da3c712923b70bae0c060388180e0f3a82. The v1.7.2 repository edition updates reader-facing
metadata only and does not replace or modify that fixed scientific baseline.

SCIENTIFIC PRESERVATION
C001-C030 = UNCHANGED
N001-N046 = UNCHANGED
V001 = UNCHANGED
E001 = UNCHANGED
E002 = UNCHANGED
SCIENTIFIC_VALUES = UNCHANGED
TOLERANCES = UNCHANGED
EVIDENCE_HASHES = UNCHANGED
CLAIM_BOUNDARIES = UNCHANGED

VERIFY
python tools/verify_publication_package.py --final-package
sha256sum -c SHA256SUMS.txt

AI SYSTEMS
PRIMARY_NON_AUTHOR_AI_SYSTEM = OpenAI ChatGPT (GPT-5.6 Thinking)
SUPPORTING_NON_AUTHOR_AI_SYSTEM = OpenAI Codex
AI_EXPERT_CERTIFICATION = NOT_PROVIDED
FINAL_RELEASE_RESPONSIBILITY = HUMAN_AUTHOR

PUBLICATION METADATA RULE
Add a report URL, DOI, or other persistent identifier only after it actually
exists, and only in a later version. Do not rewrite v1.7.1 or v1.7.2.
