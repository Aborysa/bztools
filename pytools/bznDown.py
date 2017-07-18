import re
import argparse
import utils
import os

parser = argparse.ArgumentParser(description='2XXX -> 1045')
parser.add_argument('path',help='file or directory to operate on')
parser.add_argument('out',help='Output file')


args = parser.parse_args()

DOWNGRADE_TO = "version [1] =\n1045"

V_NUM = "version \[1\] =\n\d*"

ARR_PFIX = "{}\s*\[\d+\]\s*=\n.*\n"
V_PFIX = "{}\s*=\s*.*\n"

PURGE_MAP = {
    "cloak\w*": "",
    "isCritical": "",
    "param": "param [1] =\n0\n"
}
if(os.path.isfile(args.path)):
    files = [args.path]
else:
    files = [n for n in glob.glob("{}/*.bzn".format(args.path)) if not is_binary_file(n)]

for file in files:
    try:
        with open(file,"r") as f:
            content = f.read()
            content = re.sub(V_NUM,DOWNGRADE_TO,content)
            for i, v in PURGE_MAP.items():
                content = re.sub(ARR_PFIX.format(i),v,content)
                content = re.sub(V_PFIX.format(i),v,content)

        with open(args.out or args.file,"w",newline="\r\n") as f:
            f.write(content)
    except:
        print("Failed to convert {}".format(args.file))