"""Module to look up a quote for a given time."""

import random
import sys


def random_quote(time: str):
    try:
        f = open(f"times/{time}.dat", "r")
    except FileNotFoundError:
        return None

    # Pick a random entry
    count = int(f.readline())
    pick = random.randrange(0, count)

    # Skip to the chosen entry
    for i in range(0, pick):
        f.readline()

    line = f.readline().strip()
    return dict(
        zip(["time", "quote_time", "quote", "title", "author", "nsfw"], line.split("|"))
    )


def main():
    import re

    if q := random_quote(sys.argv[1] if len(sys.argv) > 1 else "01:00"):
        text = q["quote"]
        qt = q["quote_time"]

        replace = [(re.escape(qt), r"*\g<0>*"), (r"<br.*?> *", "\n"), (r"<.*?>", "")]
        for pattern, repl in replace:
            text = re.sub(pattern, repl, text, flags=re.IGNORECASE)

        title = q["title"]
        author = q["author"]
        print(f"{text}\n\n- {title}, {author}")
    else:
        print("None")


if __name__ == "__main__":
    main()
