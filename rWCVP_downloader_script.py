"""
Download the current rWCVPdata GitHub snapshot and extract
taxonomic_mapping.rda without installing R.

Outputs:
  output/wcvp_family_order_mapping.csv
  output/rwcvp_snapshot_citation.txt
"""

import io
import json
import tarfile
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import pyreadr

REPO_API = "https://api.github.com/repos/matildabrown/rWCVPdata"
ARCHIVE_URL = "https://github.com/matildabrown/rWCVPdata/archive/refs/heads/main.tar.gz"

OUT_DIR = Path("output")
OUT_DIR.mkdir(exist_ok=True)

# 1. Get repository metadata, including the latest commit
with urllib.request.urlopen(REPO_API) as response:
    repo = json.load(response)

default_branch = repo.get("default_branch", "main")
pushed_at = repo.get("pushed_at", "unknown")
commit_sha = repo.get("default_branch", "main")

print(f"Repository default branch: {default_branch}")
print(f"Repository last pushed: {pushed_at}")
print(f"Downloading: {ARCHIVE_URL}")

# 2. Download GitHub source archive into memory
with urllib.request.urlopen(ARCHIVE_URL) as response:
    archive_bytes = response.read()

# 3. Find taxonomic_mapping.rda anywhere in the archive
mapping_bytes = None
member_name = None

with tarfile.open(fileobj=io.BytesIO(archive_bytes), mode="r:gz") as tar:
    for member in tar.getmembers():
        if member.name.endswith("taxonomic_mapping.rda"):
            fileobj = tar.extractfile(member)
            if fileobj is None:
                continue
            mapping_bytes = fileobj.read()
            member_name = member.name
            break

if mapping_bytes is None:
    raise FileNotFoundError(
        "taxonomic_mapping.rda was not found anywhere in the GitHub archive"
    )

print(f"Found: {member_name}")

# 4. Read the R data object without R
result = pyreadr.read_r(io.BytesIO(mapping_bytes))

if "taxonomic_mapping" not in result:
    raise KeyError(
        f"Expected 'taxonomic_mapping'; found: {list(result)}"
    )

mapping = result["taxonomic_mapping"]

# 5. Save the mapping as CSV
csv_path = OUT_DIR / "wcvp_family_order_mapping.csv"
mapping.to_csv(csv_path, index=False)

print(f"Saved mapping: {csv_path}")
print(f"Rows: {len(mapping)}")
print(mapping.head())

# 6. Save reproducibility/citation information
downloaded_at = datetime.now(timezone.utc).isoformat(timespec="seconds")

citation = f"""rWCVPdata GitHub snapshot citation
====================================

Package: rWCVPdata
Source: GitHub repository matildabrown/rWCVPdata
Branch: {default_branch}
Archive URL: {ARCHIVE_URL}
Repository last pushed: {pushed_at}
Downloaded: {downloaded_at}
Extracted object: {member_name}
Output CSV: {csv_path}

This is a GitHub main-branch snapshot, not necessarily a numbered
CRAN/drat release. Record the repository commit SHA and download date
for reproducibility.

Suggested methods wording:
Family-to-order relationships were obtained from the rWCVPdata GitHub
main-branch snapshot downloaded on {downloaded_at}, using the
taxonomic_mapping dataset.
"""

citation_path = OUT_DIR / "rwcvp_snapshot_citation.txt"
citation_path.write_text(citation, encoding="utf-8")

print(f"Saved citation: {citation_path}")