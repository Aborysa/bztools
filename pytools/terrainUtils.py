import struct
import numpy
from math import floor


class HeightMap:
    def __init__(self, width, length, heightData=None, max_val=0):
        self.heightData = (
            heightData if heightData != None else [0 for n in range(width * length)]
        )
        self.width = width
        self.length = length
        self.highest = max_val

    def copy(self):
        return HeightMap(self.width, self.length, list(self.heightData))

    def getMax(self):
        return self.highest

    @classmethod
    def from_data(cls, data, res, width):
        heightData, length, m = cls._parse_data(data, res, width)
        return cls(width, length, heightData, m)

    def serialize(self, res):
        return HeightMap._serialize_data(self.heightData, res, self.getWidth())

    # Takes a bz height map byte buffer and converts it to an array of height points
    @classmethod
    def _parse_data(cls, data, res, width):
        size = int(len(data) / 2)
        zone_size = 2 ** res
        length = int(size / width)
        m = 0
        obuffer = [0 for n in range(size)]
        for n in range(size):
            try:
                d_idx = n * 2
                zone = int(n / (zone_size ** 2))
                x = (n % zone_size) + zone * zone_size % width
                z = (int(n / zone_size) % zone_size) + int(
                    zone * zone_size / width
                ) * zone_size
                height = struct.unpack("<H", data[d_idx : d_idx + 2])[0]
                m = max(m, height)
                b_idx = int(x + ((length - 1) - z) * width)
                obuffer[b_idx] = height
            except Exception as e:
                break
        return obuffer, length, m

    # Takes an array of height points and converts it to a bz height map
    @classmethod
    def _serialize_data(cls, data, res, width):
        size = len(data)
        zone_size = 2 ** res
        length = int(size / width)
        obuffer = [b"" for n in range(size)]
        for n in range(size):
            try:
                zone = int(n / (zone_size ** 2))
                x = (n % zone_size) + zone * zone_size % width
                z = (int(n / zone_size) % zone_size) + int(
                    zone * zone_size / width
                ) * zone_size
                b_idx = int(x + ((length - 1) - z) * width)
                obuffer[n] = struct.pack("<H", data[b_idx])
            except Exception as e:
                print(e)
                break
        return b"".join(obuffer)

    def getWidth(self):
        return self.width

    def getLength(self):
        return self.length

    def getHeight(self, x, z):
        xx = int(min(max(x, 0), self.getWidth() - 1))
        zz = int(min(max(z, 0), self.getLength() - 1))
        return self.heightData[xx + zz * self.getWidth()]

    def getCroped(self, x, z, w, h):
        return HeightMap(
            w, h, [self.getHeight(x + n % w, z + int(n / w)) for n in range(w * h)]
        )

    def getResized(self, newW, newL, method=lambda x, z, map: map.getHeight(x, z)):
        newMap = [0 for n in range(int(newW * newL))]
        wf, lf = self.getWidth() / newW, self.getLength() / newL
        m = 0
        print("Resizing:")
        lp = 0
        for i in range(len(newMap)):
            x = i % newW
            z = int(i / newW)
            newMap[i] = int(method(int(x * wf), int(z * lf), self))
            m = max(m, newMap[i])
            p = int((i + 1) / len(newMap) * 25)
            if p != lp:
                print(
                    "[{}{}] - {:>8}/{:<8}".format(
                        "=" * p, " " * (25 - p), i + 1, len(newMap)
                    ),
                    end="\r",
                )
            lp = p
        print("\nDone")
        return HeightMap(int(newW), int(newL), newMap, m)


w_cache = {}


def createWeightGrid(size):
    if not int(size) in w_cache:
        c = size / 2
        weights = [
            size - ((c - n % size) ** 2 + (c - int(n / size)) ** 2) ** 0.5
            for n in range(0, size * size)
        ]
        w_cache[int(size)] = weights
    return w_cache[int(size)]


def AvgEdge(x, z, map, grid=5):
    cropped = map.getCroped(int(x - grid / 2), int(z - grid / 2), grid, grid)
    hdata = cropped.heightData
    weights = createWeightGrid(grid)
    mean, median = numpy.average(hdata, weights=weights), numpy.median(hdata)
    d = [n for n in hdata if (abs(n - mean) >= abs(n - median))]
    return numpy.mean([numpy.mean(d)])


def Avg(x, z, map, grid=5):
    cropped = map.getCroped(int(x - grid / 2), int(z - grid / 2), grid, grid)
    weights = createWeightGrid(grid)
    hdata = cropped.heightData

    return numpy.average(hdata, weights=weights)
