# Encode an arbitrary precision integer as bytes, ignoring machine word size and machine endianness
# format:
# - length - 1 byte
# -- high bit indicates the sign of the integer. 0 for positive, 1 for negative.
# - data   - variable size, "length" without the high bit indicates the number of bytes
import struct


def squeeze_int(x):
    # A 0 length indicates the number 0
    if x == 0:
        return bytes([0])

    # If x is negative, we encode the data for abs(x) and encode the sign in the length
    negative = False
    if x < 0:
        x = -x
        negative = True

    # Loop until we have encoded all of the necessary bytes, eliding leading zeros
    # When our working integer is 0, we are out of bytes to encode, the rest of the bytes are also 0.
    result = b''
    while x != 0:
        # Get the lowest byte and add it to the encoding, then remove that byte from the working integer
        b = x & 0xFF
        result = bytes([b]) + result
        x = x >> 8

    # Now we need to encode the length
    length = len(result)

    # A 1-byte length with a sign bit included means that we have a maximum size of 127 bytes (1016 bits), pretty big
    # This check ensures that the high bit of the length is currently set to zero.
    if length > 127:
        raise Exception("integer too long for squeeze")

    # If our integer was negative, set the high bit of the length to 1, otherwise leave it at zero.
    if negative:
        length = length | 0x80

    # Prepend the encoded bytes with the length byte that includes the sign
    return bytes([length]) + result

# Decode a squeeze-encoded integer, returning the integer and any leftover bytes that were not part of the encoding
def expand_int(x):
    # We need at least one byte to parse the format
    if len(x) == 0:
        raise Exception("Empty input")

    # Separate the length from the encoded bytes
    length = x[0]
    rest = x[1:]

    if length == 0:
        return 0, rest

    # If the high bit of the length is set, clear that bit and remember that the integer is negative
    negative = False
    if length & 0x80:
        length = length & 0x7F
        negative = True

    # This extra slice allows us to decode an integer that is part of a larger stream of values, ignoring the rest
    encoded = rest[:length]
    rest = rest[length:]

    # Loop through the bytes, adding them to the working integer
    integer = 0
    for b in encoded:
        integer = (integer << 8) + b

    # If the high bit of the length was set previously, then our integer is negative, otherwise it's positive
    if negative:
        integer = -integer

    # We return both the integer and the extra bytes at the end, allowing us to handle encoding of multiple integers
    # Multiple integers are not covered here as that is handled by a higher layer of abstraction
    return integer, rest

# This utility function is aware of the squeeze format and can read it from a connection, byte by byte
def expand_conn_int(conn):
    length = conn.readOne()[0]

    if length == 0:
        return 0

    negative = False
    if length & 0x80:
        length &= 0x7F
        negative = True

    encoded = conn.read(length)

    integer = 0
    for b in encoded:
        integer = (integer << 8) + b

    if negative:
        integer = -integer

    return integer

def squeeze_floating(i):
    if i == 0.0:
        return bytes([0])

    floatBytes = struct.pack("!d", i)
    lengthBytes = struct.pack("B", len(floatBytes))
    return lengthBytes + floatBytes

def expand_floating(bs):
    length = bs[0]
    rest = bs[1:]

    if length == 0:
        return 0.0, rest

    if length == 4:
        encoded = rest[:4]
        rest = rest[4:]

        return struct.unpack('!f', encoded)[0], rest
    elif length == 8:
        encoded = rest[:8]
        rest = rest[8:]

        return struct.unpack('!d', encoded)[0], rest
    else:
        raise Exception("invalid length")

def expand_conn_floating(conn):
    length = conn.readOne()[0]

    if length == 0:
        return 0.0

    encoded = conn.read(length)

    if length == 4:
        return struct.unpack('!f', encoded)[0]
    elif length == 8:
        return struct.unpack('!d', encoded)[0]
    else:
        raise Exception("invalid length")
