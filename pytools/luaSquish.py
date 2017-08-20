# Reads a .squish file and squishes all lua files listed
import argparse
import glob
import subprocess
import re
import os




parser = argparse.ArgumentParser(description='LF -> CRLF')
parser.add_argument('path',help='file to operate on')



args = parser.parse_args()

file = args.path
files = []

with open(file,"r") as f:
  files = [x.strip() for x in f.readlines()] 


for file in files:
  try:
    uext = os.path.realpath(file).lower().split(".")[0]
    with open("squishy","w") as f:
      f.write("Main \"{}\"\nOutput \"{}.squish\"".format(file, uext))
    subprocess.call("squish")
  except Exception as e:
    print("Could not squish file {}\n{}".format(file,e))