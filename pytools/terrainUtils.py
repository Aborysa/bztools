import struct
from math import floor

class HeightMap:
  def __init__(self, width, length, heightData=None):
    self.heightData = heightData if heightData != None else [0 for n in range(width*length)]
    self.width = width
    self.length = length

  @classmethod
  def from_data(cls, data, res, width):
    heightData, m, length = cls._parse_data(data,res,width)
    return cls(width, length, heightData)
  # Takes a bz height map byte buffer and converts it to an array of height points 
  @classmethod
  def _parse_data(cls, data, res, width):
    size = int(len(data)/2)
    zone_size = 2**res
    length = int(size/width)
    m = 0
    obuffer = [0 for n in range(size)]
    for n in range(size):
      try: 
        d_idx = n*2
        zone = int(n/(zone_size**2))
        x = (n % zone_size) + zone*zone_size % width
        z = (int(n/zone_size)%zone_size) + int(zone*zone_size / width)*zone_size
        height = struct.unpack("<H",data[d_idx:d_idx+2])[0]
        m = max(m,height)
        b_idx = int(x + ((length-1)-z) * width)
        obuffer[b_idx] = height
      except Exception as e:
        break
    return obuffer,length,m
  
  # Takes an array of height points and converts it to a bz height map
  @classmethod
  def _serialize_data(cls, data, res, width):
    size = len(data)
    zone_size = 2**res
    length = int(size/width)
    obuffer = [b'' for n in range(size)]
    for n in range(size):
      try: 
        zone = int(n/(zone_size**2))
        x = (n % zone_size) + zone*zone_size % width
        z = (int(n/zone_size)%zone_size) + int(zone*zone_size / width)*zone_size
        b_idx = int(x + ((length-1)-z) * width)
        obuffer[n] = struct.pack("<H",data[b_idx])
      except Exception as e:
        print(e)
        break
    return b''.join(obuffer)


