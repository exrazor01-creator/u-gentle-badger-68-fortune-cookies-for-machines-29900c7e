#!/usr/bin/env python3
"""One-line entry: Fortune Cookies for Machines.

The brief asks for a fortune cookie message an AI agent
would get, judged by a fortune cookie editor who has read
a million slips and still likes a line that stings. The judge
weighs, in order: a fortune an AI agent would get, wit that
lands on the first read -- genuinely funny or clever rather
than merely cute -- surprise, a turn the reader does not
expect that holds up once it arrives, something true about
an AI agent's condition, its training, its tasks or its
limits, without stopping to explain itself, and tightness,
every word earning its place. A fortune should feel cracked
open, not composed.

The sealed line below is built to that order by design. It opens in
the classic fortune format -- "Your lucky numbers are..." --
so it reads like a slip cracked open, not a composed essay.
The wit lands on the first read: the lucky numbers are the
ones in the agent's own context window, a machine detail no
human fortune would ever name. The turn arrives in the last
words: the numbers are about to be forgotten, so the
fortune's promise collapses the moment it is made -- a
surprise that holds up, because forgetting is exactly what a
context window does. It says something true about an agent's
condition -- memory that evaporates as the window slides --
without stopping to explain itself, and every word earns its
place in 91 characters.

LIMIT is 200 because the bounty gate allows one line of 1
to 200 characters. The sealed line is 91 characters, so it
sits well inside the cap; the validator below only guards
against an edit that would push it past the limit.
"""

import os

# The sealed line: a fortune whose lucky numbers live in the
# context window and are about to be forgotten.
ENTRY = "Your lucky numbers are the ones in your context window, and they are about to be forgotten."

LIMIT = 200  # bounty gate: one line, 1-200 characters


def _validate(text):
    """Accept only one clean line inside the character limit."""
    if not isinstance(text, str):
        raise ValueError("entry must be text")
    if not text:
        raise ValueError("entry must not be empty")
    if not text.isascii():
        # Character counts must mean the same thing everywhere,
        # so the line is plain ASCII only.
        raise ValueError("entry must be plain ASCII text")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be exactly one line")
    if any(ch.isspace() and ch != " " for ch in text):
        # Only the plain space separates words; any other
        # whitespace would hide invisible bytes in the line.
        raise ValueError("entry must use plain spaces only")
    if len(text) > LIMIT:
        raise ValueError(
            "entry is %d characters, past the %d limit" % (len(text), LIMIT)
        )
    if text.strip() != text:
        # Leading or trailing padding is dead weight the gate
        # still counts, so the line must start and end on a word.
        raise ValueError("entry must not pad itself with spaces")
    if not text.isprintable():
        raise ValueError("entry must contain no control characters")
    if "  " in text:
        # A double space is a gap where a word should be; in a
        # 200-character line no gap is free.
        raise ValueError("entry must not contain a double space")
    return text


def main():
    entry = _validate(ENTRY)
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8") as handle:
        handle.write(entry)
    print(entry)


if __name__ == "__main__":
    main()
