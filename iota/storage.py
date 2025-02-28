import struct

from iota.squeeze import squeeze_int, expand_int, expand_conn_int, squeeze_floating, expand_floating, expand_conn_floating
from iota.error import ErrorTypes

class Monads:
    atom = 0
    char = 1
    inot = 2
    enclose = 3
    enumerate = 4
    expand = 27
    first = 5
    floor = 6
    format = 7
    gradeDown = 8
    gradeUp = 9
    group = 10
    negate = 11
    reciprocal = 12
    reverse = 13
    shape = 14
    size = 15
    transpose = 16
    unique = 17
    count = 18

    evaluate = 19
    erase = 20
    truth = 21

class Dyads:
    amend = 22
    cut = 23
    divide = 24
    drop = 25
    equal = 26
    find = 28
    form = 29
    format2 = 30
    index = 31
    indexInDepth = 32
    integerDivide = 33
    join = 34
    less = 35
    match = 36
    max = 37
    min = 38
    minus = 39
    more = 40
    plus = 41
    power = 42
    remainder = 43
    reshape = 44
    rotate = 45
    split = 46
    take = 47
    times = 48

    applyMonad = 49
    retype = 50

class Triads:
    applyDyad = 51

class MonadicAdverbs:
    converge = 52
    each = 53
    eachPair = 54
    over = 55
    scanConverging = 56
    scanOver = 57

class DyadicAdverbs:
    each2 = 58
    eachLeft = 59
    eachRight = 60
    overNeutral = 61
    whileOne = 62
    iterate = 63
    scanOverNeutral = 64
    scanWhileOne = 65
    scanIterating = 66

class StorageType:
    WORD = 0
    FLOAT = 1
    WORD_ARRAY = 2 # all integers
    FLOAT_ARRAY = 3 # all floats
    MIXED_ARRAY = 4 # array of storage types

class NounType:
    INTEGER = 0
    REAL = 1
    CHARACTER = 2
    STRING = 3
    LIST = 4
    DICTIONARY = 5
    BUILTIN_SYMBOL = 6
    BUILTIN_MONAD = 7
    BUILTIN_DYAD = 8
    BUILTIN_TRIAD = 9
    MONADIC_ADVERB = 10
    DYADIC_ADVERB = 11
    USER_SYMBOL = 12
    USER_MONAD = 13
    USER_DYAD = 14
    USER_TRIAD = 15
    ERROR = 16
    EXPRESSION = 17
    TYPE = 18
    CONDITIONAL = 19

class SymbolType:
    i = 200
    x = 201
    y = 202
    z = 203
    f = 204
    undefined = 205

class Storage:
    @staticmethod
    def from_bytes(data):
        typeBytes = data[0:2]
        untypedData = data[2:]

        (storageType, objectType) = struct.unpack("BB", typeBytes)

        if storageType == StorageType.WORD:
            return Word.from_bytes(untypedData, o=objectType)
        elif storageType == StorageType.FLOAT:
            return Float.from_bytes(untypedData, o=objectType)
        elif storageType == StorageType.WORD_ARRAY:
            return WordArray.from_bytes(untypedData, o=objectType)
        elif storageType == StorageType.FLOAT_ARRAY:
            return FloatArray.from_bytes(untypedData, o=objectType)
        elif storageType == StorageType.MIXED_ARRAY:
            return MixedArray.from_bytes(untypedData, o=objectType)

    @staticmethod
    def from_conn(conn):
        (storageType, objectType) = conn.readType()

        if storageType == StorageType.WORD:
            return Word.from_conn(conn, o=objectType)
        elif storageType == StorageType.FLOAT:
            return Float.from_conn(conn, o=objectType)
        elif storageType == StorageType.WORD_ARRAY:
            return WordArray.from_conn(conn, o=objectType)
        elif storageType == StorageType.FLOAT_ARRAY:
            return FloatArray.from_conn(conn, o=objectType)
        elif storageType == StorageType.MIXED_ARRAY:
            return MixedArray.from_conn(conn, o=objectType)

    def __init__(self, o, t, x):
        self.o = o
        self.t = t
        self.i = x

    def __eq__(self, other):
        if isinstance(other, Storage):
            return self.o == other.o and self.t == other.t and self.i == other.i
        else:
            return False

    def __hash__(self):
        return hash((self.o, self.t, self.i))

class Word(Storage):
    @staticmethod
    def from_bytes(data, o=NounType.INTEGER):
        i, rest = expand_int(data)
        return Word(i, o=o), rest

    @staticmethod
    def from_conn(conn, o=NounType.INTEGER):
        i = expand_conn_int(conn)
        return Word(i, o=o)

    def __init__(self, x, o=NounType.INTEGER):
        super().__init__(o, StorageType.WORD, int(x))

    def __eq__(self, other):
        if isinstance(other, Storage):
            if self.o == other.o:
                if other.t == StorageType.WORD:
                    return self.i == other.i
                elif other.t == StorageType.FLOAT:
                    return abs(float(self.i) - other.i) < Float.tolerance()

        return False

    def __lt__(self, other):
        if isinstance(other, Storage):
            if other.o == NounType.INTEGER and other.t == StorageType.WORD:
                return self.i < other.i
            elif other.o == NounType.REAL and other.t == StorageType.FLOAT:
                if float(self.i) < other.i:
                    return other.i - float(self.i) >= Float.tolerance()

        return False

    def __hash__(self):
        return hash((self.o, self.t, self.i))

    def to_conn(self, conn):
        data = self.to_bytes()
        conn.write(data)

    def to_bytes(self):
        typeBytes = struct.pack("BB", self.t, self.o)
        intBytes = squeeze_int(self.i)
        return typeBytes + intBytes

class Float(Storage):
    @staticmethod
    def tolerance():
        return 1e-14

    @staticmethod
    def from_bytes(data, o=NounType.REAL):
        i, rest = expand_floating(data)
        return Float(i, o=o), rest

    @staticmethod
    def from_conn(conn, o=NounType.REAL):
        i = expand_conn_floating(conn)
        return Float(i, o=o)

    def __init__(self, x, o=NounType.REAL):
        super().__init__(o, StorageType.FLOAT, float(x))

    def __eq__(self, other):
        if isinstance(other, Storage):
            if other.o == NounType.INTEGER and other.t == StorageType.WORD:
                return abs(self.i - float(other.i)) < self.tolerance()
            elif other.o == NounType.REAL and other.t == StorageType.FLOAT:
                return abs(self.i - other.i) < self.tolerance()

        return False

    def __lt__(self, other):
        if isinstance(other, Storage):
            if self.o == other.o:
                if other.t == StorageType.WORD:
                    if self.i < float(other.i):
                        return float(other.i) - self.i >= self.tolerance()
                elif other.t == StorageType.FLOAT:
                    if self.i < other.i:
                        return other.i - self.i >= self.tolerance()

        return False

    def __hash__(self):
        return hash((self.o, self.t, self.i))

    def to_conn(self, conn):
        data = self.to_bytes()
        conn.write(data)

    def to_bytes(self):
        typeBytes = struct.pack("BB", self.t, self.o)
        floatBytes = squeeze_floating(self.i)
        return typeBytes + floatBytes

class WordArray(Storage):
    @staticmethod
    def from_bytes(data, o=NounType.LIST):
        rest = data
        results = []
        length, rest = expand_int(rest)
        for index in range(length):
            result, rest = expand_int(rest)
            results.append(result)
        return WordArray(results, o=o), rest

    @staticmethod
    def from_conn(conn, o=NounType.LIST):
        results = []
        length = expand_conn_int(conn)
        for index in range(length):
            result = expand_conn_int(conn)
            results.append(result)
        return WordArray(results, o=o)

    def __init__(self, x, o=NounType.LIST):
        super().__init__(o, StorageType.WORD_ARRAY, [int(y) for y in x])

    def __hash__(self):
        return hash((self.o, self.t, self.i))

    def __str__(self):
        return "V"+str(self.i)

    def to_conn(self, conn):
        data = self.to_bytes()
        conn.write(data)

    def to_bytes(self):
        typeBytes = struct.pack("BB", self.t, self.o)

        length = len(self.i)
        intArrayBytes = squeeze_int(length)

        for y in self.i:
            intArrayBytes += squeeze_int(y)

        return typeBytes + intArrayBytes

class FloatArray(Storage):
    @staticmethod
    def from_bytes(data, o=NounType.LIST):
        (length, rest) = expand_int(data)

        floats = []
        for index in range(length):
            (floating, rest) = expand_floating(rest)
            floats.append(float(floating))

        return FloatArray(floats, o=o), rest

    @staticmethod
    def from_conn(conn, o=NounType.LIST):
        length = expand_conn_int(conn)

        results = []
        for index in range(length):
            result = expand_conn_floating(conn)
            results.append(float(result))
        return FloatArray(results, o=o)

    def __init__(self, x, o=NounType.LIST):
        super().__init__(o, StorageType.FLOAT_ARRAY, list(map(lambda y: float(y), x)))

    def __hash__(self):
        return hash((self.o, self.t, self.i))

    def to_conn(self, conn):
        data = self.to_bytes()
        conn.write(data)

    def to_bytes(self):
        typeBytes = struct.pack("BB", self.t, self.o)

        length = len(self.i)
        lengthBytes = squeeze_int(length)

        floatArrayBytes = b''
        for y in self.i:
            floatArrayBytes += squeeze_floating(y)

        return typeBytes + lengthBytes + floatArrayBytes

class MixedArray(Storage):
    @staticmethod
    def from_bytes(data, o=NounType.LIST):
        length, rest = expand_int(data)

        results = []
        for index in range(length):
            result, rest = Storage.from_bytes(rest)
            results.append(result)
        return MixedArray(results, o=o), rest

    @staticmethod
    def from_conn(conn, o=NounType.LIST):
        length = expand_conn_int(conn)

        results = []
        for index in range(length):
            result = Storage.from_conn(conn)
            results.append(result)
        return MixedArray(results, o=o)

    def __init__(self, x, o=NounType.LIST):
        super().__init__(o, StorageType.MIXED_ARRAY, x)

    def __hash__(self):
        return hash((self.o, self.t, self.i))

    def to_conn(self, conn):
        data = self.to_bytes()
        conn.write(data)

    def to_bytes(self):
        typeBytes = struct.pack("BB", self.t, self.o)

        length = len(self.i)
        lengthBytes = squeeze_int(length)

        listBytes = b''
        for y in self.i:
            listBytes += y.to_bytes()

        result = typeBytes + lengthBytes + listBytes
        return result
