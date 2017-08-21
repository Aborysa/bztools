# Reads a .squish file and squishes all lua files listed
import argparse
import glob
import subprocess
import re
import os




parser = argparse.ArgumentParser(description='LF -> CRLF')
parser.add_argument('path',help='directory to operate on')



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
    subprocess.call("make_squishy {}".format(file))
    os.rename("squishy.new", "squishy")
     with open("squishy","a") as f:
      f.write("\nMain \"{}\"\nOutput \"{}.squished\"\n".format(file, uext))
      squished.append("{}.squished".format(uext))
    subprocess.call("squish")
  except Exception as e:
    print("Could not squish file {}\n{}".format(f,e))


# Clean up, remove all lua files
for file in glob.glob("*.lua"):
  if os.path.exists(file):
    os.remove(file)

for file in squished:
  uext = file.split(".")[0]
  os.rename(file,"{}.lua".format(uext))