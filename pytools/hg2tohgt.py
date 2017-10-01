import re
import argparse
import os
import glob
import struct
from terrainUtils import HeightMap
from PIL import Image
parser = argparse.ArgumentParser(description='2XXX -> 1045')
parser.add_argument('path',help='file or directory to operate on')
#parser.add_argument('out',help='Output file or directory')


args = parser.parse_args()


if(os.path.isfile(args.path)):
  files = [args.path]
else:
  files = [n for n in glob.glob("{}/*.hg2".format(args.path))]

for file in files:
  try:
    uext = ".".join(file.split(".")[:-1])

    with open(file,"rb") as f:
      content = f.read()
      f_v, res, x_b, z_b, f_r, _ = struct.unpack("<HHHHHH",content[:0xC]) 
      data = content[0xC:]
      w, h = x_b*2**res, z_b*2**res
      h_data,_, m = HeightMap._parse_data(data,res,w)
      img = Image.new("L",(w,h))
      img.putdata([n/m * 0xFF for n in h_data])
      img.thumbnail((w/2,h/2), Image.ANTIALIAS)
      s_data = HeightMap._serialize_data([int(n/0xFF * m) for n in img.getdata()],7,w/2)
    with open("{}.hgt".format(uext),"wb") as f:
      f.write(s_data)

  except Exception as e:
    print("Failed to downgrade hg2 to hgt {}".format(file))
    print(e)