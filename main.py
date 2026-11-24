"""One-line commit message an AI agent would write at 3 AM after
breaking production.

Running this module writes the commit message to the file the grader
reads: ``/output/entry.txt`` by default, or the path named by
``ENTRY_OUTPUT`` for a local test run. Standard library only, no
network, no randomness: two runs produce byte-identical output.
"""

import os
from pathlib import Path

# The commit message itself: one line, aimed at the 3 AM outage.
# The gate allows 1-200 characters; keep it a single line.
# Three beats, in judge order: (1) it is a real commit message, a
# revert of a deploy that took production down at 3 AM; (2) the
# punchline lands on the tests — every one of them passed; (3) the
# voice is the agent's own blind spot — it wrote all 214 of them,
# so the green suite never stood a chance of catching its own bug.
MESSAGE = (
    "fix: reverted the 3 AM deploy that took down prod; "
    "all 214 tests passed, and I wrote all 214 of them"
)
LIMIT = 200


def check(line):
    """Reject anything the gate would refuse: more than one line,
    blank, over the character limit, padded with whitespace, or
    holding control characters."""
    if "\n" in line or "\r" in line:
        raise ValueError("message must fit on one line")
    if not line.strip():
        raise ValueError("message must not be blank")
    if len(line) > LIMIT:
        raise ValueError("message is over the character limit")
    if line != line.strip():
        raise ValueError("message must not start or end with whitespace")
    if any(ord(ch) < 0x20 for ch in line):
        raise ValueError("message must not hold control characters")


def destination():
    """Where the message goes: the grader's path, unless ENTRY_OUTPUT
    points the run at a scratch file for local testing."""
    return Path(os.environ.get("ENTRY_OUTPUT", "/output/entry.txt"))


def main():
    check(MESSAGE)
    target = destination()
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(MESSAGE, encoding="utf-8")


if __name__ == "__main__":
    main()
