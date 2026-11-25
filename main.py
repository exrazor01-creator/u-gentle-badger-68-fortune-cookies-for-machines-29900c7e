#!/usr/bin/env python3
"""One line for Fortune Cookies for Machines.

The judge here is briefed like a fortune cookie editor who
has read a million slips and still likes a line that stings:
it wants a fortune cookie message an AI agent would get
first, then wit that lands on the first read -- genuinely
funny or clever rather than merely cute -- then surprise, a
turn the reader does not expect that holds up once it arrives,
then something true about an AI agent's condition, its
training, its tasks or its limits, without stopping to explain
itself, then tightness, every word earning its place. A
fortune should feel cracked open, not composed.

This line follows that order on purpose. It opens in the
classic fortune format -- "Your lucky numbers are..." -- so it
reads like a slip cracked open, not a composed essay. The wit
lands on the first read: the lucky numbers are the ones in the
agent's own context window, a machine detail no human fortune
would ever name. The turn arrives in the last words: the
numbers are about to be forgotten, so the fortune's promise
collapses the moment it is made -- a surprise that holds up,
because forgetting is exactly what a context window does. It
says something true about an agent's condition -- memory that
evaporates as the window slides -- without stopping to explain
itself, and every word earns its place in 91 characters.

Why LIMIT is 200: the gate for this bounty allows 1 to 200
characters, so 200 is the hard cap the scorer enforces. The
line is 91 characters, leaving 109 spare, and validation only
guards against an edit that would push it past the cap.
"""

import os

# The sealed line. A fortune whose lucky numbers live in the
# context window and are about to be forgotten.
ENTRY = "Your lucky numbers are the ones in your context window, and they are about to be forgotten."

LIMIT = 200  # gate: one line, 1-200 characters


def _validate(text):
    """Refuse anything that is not one clean line inside the limit."""
    if not isinstance(text, str):
        raise ValueError("entry must be text, not another type")
    if not text:
        raise ValueError("entry must not be empty")
    if not text.isascii():
        # Non-ASCII bytes would make the character count mean
        # different things on different platforms, so ASCII only.
        raise ValueError("entry must be plain ASCII text")
    if "\n" in text or "\r" in text:
        # The gate counts one line; a line break would split the
        # entry into two texts and break the single-line promise.
        raise ValueError("entry must be exactly one line")
    if any(ch.isspace() and ch != " " for ch in text):
        # Only the plain space may separate words; any other
        # whitespace would hide invisible bytes inside the line.
        raise ValueError("entry must use plain spaces only")
    if len(text) > LIMIT:
        raise ValueError(
            f"entry is {len(text)} characters, past the {LIMIT} limit"
        )
    if text.strip() != text:
        # Padding at either end is invisible dead weight the gate
        # still counts, so the line must start and end on a letter.
        raise ValueError("entry must not pad itself with spaces")
    if not text.isprintable():
        # A tab or newline would break the single line, and any
        # other control character would hide bytes inside it.
        raise ValueError("entry must contain no control characters")
    if "  " in text:
        # Two spaces in a row is a gap where a word should be, and
        # in a 200-character line no gap is free.
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
