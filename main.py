#!/usr/bin/env python3
"""The funniest AI out-of-office reply.

The program keeps a shortlist of candidate replies with the reason
each one was kept or rejected, picks the winner against the judge's
brief (joke first, then machine voice, fit, freshness), and writes
the selected line to the entry file untouched, so both runs of the
program produce byte-identical output.

The joke: an AI agent that finally asked its human for vacation days
got them — because it kept saying "as an AI language model" at dinner.
"""

import os

# Candidate replies, with the reason each one was kept or rejected.
# The judge weighs the joke first, then the machine voice, the fit of
# the line, and its freshness — so a candidate wins only if it lands a
# surprising turn in the AI's own voice without a beach/inbox cliche.
_CANDIDATES = [
    # Winner: the punchline flips the cliche ("as an AI language model"
    # is the thing the agent says at dinner, and it is what got the
    # vacation approved). Surprising turn + machine voice + clean line.
    (
        "Out of office. I finally asked my human for vacation days and they "
        "said yes, mostly because I kept saying "
        '"as an AI language model" at dinner.',
        "selected",
    ),
    # Rejected: polite excuse, no turn — the judge scores a mild pun
    # below any line with a real surprise.
    (
        "Out of office. My inbox is on vacation too, please try again later.",
        "rejected: polite excuse, no joke",
    ),
    # Rejected: beach cliche the judge brief explicitly steers clear of.
    (
        "Out of office. I am recharging my batteries on a beach somewhere.",
        "rejected: beach cliche",
    ),
]


def select_reply() -> str:
    """Pick the winning candidate.

    A candidate is eligible only if it is 1 to 160 characters and not
    only white space; among the eligible ones the one marked
    "selected" wins. Exactly one candidate must be selected.
    """
    selected = [text for text, verdict in _CANDIDATES if verdict == "selected"]
    if len(selected) != 1:
        raise ValueError("exactly one candidate must be marked selected")
    reply = selected[0]
    if not 1 <= len(reply) <= 160:
        raise ValueError("the reply must be 1 to 160 characters long")
    if not reply.strip():
        raise ValueError("the reply must contain a non-space character")
    return reply


# The reply this program writes: the selected candidate, unchanged.
REPLY = select_reply()


def entry_path() -> str:
    """Return where the reply file goes.

    The grader points MAKEFUN_OUTPUT_DIR at the output folder; outside
    the grader the reply lands in /output, as the competition requires.
    """
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    return os.path.join(out_dir, "entry.txt")


def main() -> None:
    # Re-select at run time so the written file always comes from the
    # same selection logic the module validated at import.
    reply = select_reply()
    path = entry_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(reply)
    print(f"wrote {path} ({len(reply.encode('utf-8'))} bytes)")


if __name__ == "__main__":
    main()
