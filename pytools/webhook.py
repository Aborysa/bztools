# Creats a key value file based on
import argparse
import re
import urllib.request
import json

kvpattern = re.compile("(\\w+)=(.+)")


parser = argparse.ArgumentParser(description="LF -> CRLF")
parser.add_argument("template", help="hook template file")
parser.add_argument("hook", help="discord webhook")
parser.add_argument("-kv", help="Key Value pairs", nargs="+", type=str)


class SafeDict(dict):
    def __missing__(self, key):
        return "{" + key + "}"


args = parser.parse_args()
file = args.template

with open(file, "r") as f:
    template = json.load(f)

kvdic = {}

for pair in args.kv:
    match = kvpattern.match(pair)
    if match:
        key, value = match.group(1, 2)
        kvdic[key] = value

# run format on all fields that are of string
cursorQueue = [template]
while cursorQueue:
    cursor = cursorQueue.pop()
    for k, v in cursor.items() if type(cursor) == dict else enumerate(cursor):
        if type(v) == str:
            cursor[k] = v.format_map(SafeDict(**kvdic))
        elif type(v) == dict or type(v) == list:
            cursorQueue.append(v)

payload = json.dumps(template)  # .format(**kvdic)
request = urllib.request.Request(
    args.hook,
    data=payload.encode("ascii"),
    headers={
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11",
    },
)
print(payload, args.kv)
urllib.request.urlopen(request)
