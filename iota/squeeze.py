def squeeze(x):
    if x == 0:
        return b"\x00"
    elif x < 0:
        length = (x.bit_length() + 8) // 8
        if length > 127:
            raise Exception("integer too long for squeeze")
        data = (-x).to_bytes(length, 'big', signed=False)
        lengthBytes = (length | 0x80).to_bytes(1, 'big', signed=False)
        return lengthBytes + data
    else: # x > 0
        length = (x.bit_length() + 7) // 8
        if length > 127:
            raise Exception("integer too long for squeeze")
        data = x.to_bytes(length, 'big', signed=False)
        lengthBytes = length.to_bytes(1, 'big', signed=False)
        return lengthBytes + data

def read_conn(conn):
    lengthByte = conn.read(1)
    if len(lengthByte) == 0:
        raise Exception("Empty read")

    length = int.from_bytes(lengthByte, 'big')
    if length < 0:
        length = -length
    rest = conn.read(length)

    if len(rest) != length:
        raise Exception("Bad read")

    return lengthByte + rest

def expand(x):
    if len(x) == 0:
        raise Exception("Empty input")

    lengthBytes = x[0:1]
    rest = x[1:]
    length = int.from_bytes(lengthBytes, 'big')
    negative = False
    if length & 0x80:
        length = length & 0x7F
        negative = True

    data = rest[:length]
    rest = rest[length:]

    y = int.from_bytes(data, 'big')

    if negative:
        y = -y

    return y, rest
