# Fixes CRLF issues for battlezone
# Operates on all files in folder or specific files

import mimetypes
import argparse
import re
import glob
import os
from utils import is_binary_file

parser = argparse.ArgumentParser(description='LF -> CRLF')
parser.add_argument('path',help='file or directory to operate on')

args = parser.parse_args()
if(os.path.isfile(args.path)):
  files = [args.path]
else:
  files = [n for n in glob.glob("{}/*".format(args.path)) if not is_binary_file(n)]

for file in files:
  try:
    with open(file,'r') as f:
      content = f.read()
    with open(file,'w',newline='\r\n') as f:
      f.write(content)
  except:
    print("Could not read or convert file {}".format(file))
