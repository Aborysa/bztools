class bznParser:
  __init__(b_stream):
    b_stream.seek(0x0F)
    self.version = b_stream.read(4)
    b_stream.seek(0x27)
    self.binary = b_stream.read(4).lower() == b"true"
    self.msn_name = b_stream.read()