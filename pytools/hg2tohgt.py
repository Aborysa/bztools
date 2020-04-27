import re
import argparse
import os
import glob
import struct
from terrainUtils import HeightMap, Avg, AvgEdge
from PIL import Image

parser = argparse.ArgumentParser(description="Converts between hg2, hgt and images")
parser.add_argument("path", help="file or directory to operate on")
# parser.add_argument('out',help='Output file or directory')


args = parser.parse_args()


if os.path.isfile(args.path):
    files = [args.path]
else:
    files = [n for n in glob.glob("{}/*.hg2".format(args.path))]

for file in files:
    try:
        uext = ".".join(file.split(".")[:-1])

        with open(file, "rb") as f:
            content = f.read()
            f_v, res, x_b, z_b, f_r, _ = struct.unpack("<HHHHHH", content[:0xC])
            data = content[0xC:]
            w, h = x_b * 2 ** res, z_b * 2 ** res
            h_data = HeightMap.from_data(data, res, w)

            m = h_data.getMax()
            h_data2 = h_data.getResized(w / 2, h / 2, Avg)
            s_data = h_data2.serialize(7)
        with open("{}.hgt".format(uext), "wb") as f:
            f.write(s_data)

    except Exception as e:
        print("Failed to downgrade hg2 to hgt {}".format(file))
        print(e)
