# Creats a key value file based on
import vdf
import argparse
import glob
import subprocess
import re
import os




parser = argparse.ArgumentParser(description='LF -> CRLF')
parser.add_argument('username',help='steam username')
parser.add_argument('password',help='steam password')
parser.add_argument('vdf',help='vdf keyvalue file')
parser.add_argument('-steamguard', help='optional steamguard code')
optional_args = ['contentfolder','previewfile','title','changenote','publishedfileid']

for i in optional_args:
  parser.add_argument('-{}'.format(i))

args = parser.parse_args()

username = args.username
password = args.password

sguard = args.steamguard or "" 

file = args.vdf

with open(file, "r") as f:
  d = vdf.load(f)

wsitem = d["workshopitem"]


args = vars(args)
for i in optional_args:
  if args[i]:
    v = wsitem[i].format(args[i])
    wsitem[i] = v
    print("Setting {} to {}".format(i, v))

with open("./tmp_vdf.vdf", "w") as f:
  vdf.dump(d, f, pretty=True)



subprocess.call('steamcmd +login {} {} {} +workshop_build_item {} +quit'.format(username, password, sguard, os.path.realpath('./tmp_vdf.vdf')), shell=True)