from __future__ import annotations

import os
import re
import sys


ALLOWED_KEYS = {"PIPE-1", "PIPE-2", "PIPE-3"}
PATTERN = re.compile(r"\b([A-Z]+-\d+)\b")


def extract_keys(text: str) -> set[str]:
    return set(PATTERN.findall(text or ""))


def main() -> int:
    values = [
        os.getenv("BRANCH_NAME", ""),
        os.getenv("PR_TITLE", ""),
        os.getenv("COMMIT_MESSAGE", ""),
    ]

    found = set()
    for value in values:
        found |= extract_keys(value)

    matched = found & ALLOWED_KEYS

    if not matched:
        print("ERROR: No allowed JIRA key found.")
        print(f"Expected one of: {sorted(ALLOWED_KEYS)}")
        print(f"Scanned values: {values}")
        return 1

    print(f"JIRA validation passed. Found keys: {sorted(matched)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())