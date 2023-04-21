"""Converts a time into English."""

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

import time

digits = [
    "zero",
    "one",
    "two",
    "three",
    "four",
    "five",
    "six",
    "seven",
    "eight",
    "nine",
    "ten",
    "eleven",
    "twelve",
    "thirteen",
    "fourteen",
    "fifteen",
    "sixteen",
    "seventeen",
    "eighteen",
    "nineteen",
]

tens = ["", "ten", "twenty", "thirty", "forty", "fifty"]


def word(n):
    if n < 20:
        return digits[n]

    t = int(n / 10)
    d = n % 10
    if d == 0:
        return tens[t]
    else:
        return tens[t] + "-" + digits[d]


def time_words(h: int, m: int, s: int):
    timestr = word(h - 12 if h > 12 else h)

    if m == 0:
        timestr += " o'clock"
    elif m < 10:
        timestr += " oh " + word(m)
    else:
        timestr += " " + word(m)

    if s == 1:
        timestr += " and one second"
    elif s > 0:
        timestr += " and " + word(s) + " seconds"

    if h > 17:
        timestr += " in the evening"
    elif h > 11:
        timestr += " in the afternoon"
    else:
        timestr += " in the morning"

    return timestr


def main():
    local_time = time.localtime()
    print(time_words(local_time.tm_hour, local_time.tm_min, local_time.tm_sec))


if __name__ == "__main__":
    main()
