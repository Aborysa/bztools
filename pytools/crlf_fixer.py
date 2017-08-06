# Fixes CRLF issues for battlezone
# Operates on all files in folder or specific files

import mimetypes
import argparse
import codecs
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
    with codecs.open(file,'r',encoding='utf-8') as f:
      content = f.read()
    with codecs.open(file,'w',newline='\r\n',encoding='utf-8') as f:
      f.write(content)
  except Exception as e:
    print("Could not read or convert file {}\n{}".format(file,e))
