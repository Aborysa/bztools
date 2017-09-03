# Reads a .squish file and squishes all lua files listed
import argparse
import glob
import subprocess
import re
import os




parser = argparse.ArgumentParser(description='LF -> CRLF')
parser.add_argument('path',help='directory to operate on')
parser.add_argument('-r', action='store_true')


args = parser.parse_args()

path = args.path
files = []

os.chdir(path)

with open(".squish","r") as f:
  files = [x.strip() for x in f.readlines()] 


squished = []

for file in files:
  try:
    uext = file.split(".")[0]
    subprocess.call("make_squishy {}".format(file),shell=True)
    os.rename("squishy.new", "squishy")
    with open("squishy","a") as f:
      f.write("\nOutput \"{}.squished\"\n".format(uext))
      squished.append("{}.squished".format(uext))
    subprocess.call("squish --no-minify",shell=True)
  except Exception as e:
    print("Could not squish file {}\n{}".format(file,e))


# Clean up, remove all lua files
if(args.r):
  for file in glob.glob("*.lua"):
    if os.path.exists(file):
      os.remove(file)

  for file in squished:
    uext = file.split(".")[0]
    os.rename(file,"{}.lua".format(uext))