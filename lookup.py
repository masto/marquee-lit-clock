"""Module to look up a quote for a given time."""

# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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
