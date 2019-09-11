#!/usr/bin/env python

"""Display a system notification on macOS.

osascript -e 'display notification "Lorem ipsum dolor sit amet" with title "Title"
"""

from __future__ import print_function

import argparse
import json
import subprocess
import sys


def notify(title, message):
    apple_script = "display notification {} with title {}".format(
        json.dumps(message), json.dumps(title)
    )
    subprocess.check_call(["osascript", "-e", apple_script])


def get_args():
    parser = argparse.ArgumentParser(
        description="Display a system notification on macOS.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "title", nargs="?", default="Interruption", help="Notification title."
    )
    parser.add_argument(
        "messages", metavar="message", nargs=1, help="Notification message."
    )

    args = parser.parse_args()
    message, = args.messages
    return args.title, message


def main():
    if sys.platform != "darwin":
        print("This tool is intended for macOS", file=sys.stderr)
        sys.exit(1)

    title, message = get_args()
    notify(title, message)


if __name__ == "__main__":
    main()
