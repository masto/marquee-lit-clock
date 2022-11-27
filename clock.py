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

# LED marquee literature clock

import argparse
import colorsys
import json
import random
import re
import time

import paho.mqtt.client as mqtt
from unidecode import unidecode

from lookup import random_quote
from word_clock import time_words


def random_hue():
    return random.random()


def hue_code(hue: float):
    rgb = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
    return f"{{#{int(rgb[0]*255):02x}{int(rgb[1]*255):02x}{int(rgb[2]*255):02x}}}"


def on_ready(client, userdata, message):
    # Skip "pre-queuing". This is real-time(-ish).
    payload = json.loads(message.payload)
    if not payload["ready"]:
        return

    # Random color for the main text
    hue = random_hue()
    main_color = hue_code(hue)

    # Try to get the time as a literature quote
    message = ""
    local_time = time.localtime()
    time_str = time.strftime("%H:%M", local_time)
    q = random_quote(time_str)

    if q:
        quote = q["quote"]
        qt = q["quote_time"]

        # Pick a contrasting color for the time
        time_color = hue_code(hue + colorsys.ONE_THIRD)

        # Make some adjustments to the text
        replace = [
            # Highlight the time
            (re.escape(qt), f"{time_color}\\g<0>{main_color}"),
            # Clean up HTML in the source data
            (r"<br.*?> *", " "),
            (r"<.*?>", ""),
            # Tidy up
            (r" +", " "),
            (r" +\.", "."),
            (r" +,", ","),
        ]
        for pattern, repl in replace:
            quote = re.sub(pattern, repl, quote, flags=re.IGNORECASE)

        # Pick a contrasting color for the citation
        cite_color = hue_code(hue + colorsys.TWO_THIRD)

        # Replace non-ASCII characters
        quote = unidecode(quote)
        title = unidecode(q["title"])
        author = unidecode(q["author"])
        message = f"{main_color}{quote} {cite_color}- {title}, {author}"
    else:
        # If none found, fall back to a word clock
        words = time_words(local_time.tm_hour, local_time.tm_min, local_time.tm_sec)
        message = f"{main_color}It's {words}."

    print(message)

    base_topic = userdata["base_topic"]
    client.publish(f"{base_topic}/text", json.dumps({"text": message}))


def on_connect(client, userdata, flags, rc):
    if rc != 0:
        sys.exit(f"MQTT failed to connect: {mqtt.connack_string(rc)}")


def on_disconnect(client, userdata, rc):
    if rc != 0:
        sys.exit(f"MQTT disconnected: {mqtt.connack_string(rc)}")


def get_args():
    parser = argparse.ArgumentParser(
        description="Shows the time using literature quotes."
    )
    parser.add_argument("--marquee_node", required=True, help="MQTT marquee node name")
    parser.add_argument("--mqtt_server", default="mqtt", help="MQTT server name")
    parser.add_argument("--mqtt_user", help="MQTT auth user name")
    parser.add_argument("--mqtt_pass", help="MQTT auth password")

    args = parser.parse_args()

    return args


def main():
    args = get_args()

    base_topic = f"marquee/{args.marquee_node}"

    client = mqtt.Client(userdata={"base_topic": base_topic})
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    if args.mqtt_user:
        client.username_pw_set(args.mqtt_user, args.mqtt_pass)
    client.connect(args.mqtt_server)

    client.subscribe(f"{base_topic}/ready")
    client.message_callback_add(f"{base_topic}/ready", on_ready)

    client.loop_forever()


if __name__ == "__main__":
    main()
