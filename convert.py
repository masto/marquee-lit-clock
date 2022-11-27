# Convert litclock_annotated.csv to a series of individual files,
# one per minute. Each file contains a line count, followed by the lines
# from the original file.
#
# Obtain the source file from https://github.com/JohannesNE/literature-clock

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

import re


def write_file(time: str, lines: list[str]):
    print(f"writing {len(lines)} lines for {time}")

    # We're using this to synthesize a file name, so just make sure it looks
    # legitimate.
    if not re.match(r"\d{2}:\d{2}", time):
        raise ValueError(f"Unexpected time format: {time}")

    out_file = open(f"times/{time}.dat", "w")
    out_file.write(str(len(lines)) + "\n")
    out_file.writelines(lines)
    out_file.close


def main():
    in_file = open("litclock_annotated.csv", "r")

    prev_time = ""
    lines = []

    while line := in_file.readline():
        time = line.split("|")[0]
        if time == prev_time:
            # Continue accummulating lines while we see the same time
            lines.append(line)
        else:
            # Special-case first line: don't write out anything
            if prev_time != "":
                write_file(prev_time, lines)
            # Start accumulating lines for the new time
            prev_time = time
            lines = [line]

    # Anything left over at the end?
    if lines:
        write_file(prev_time, lines)

    in_file.close()


if __name__ == "__main__":
    main()
