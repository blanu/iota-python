import struct

from iota.squeeze import squeeze, expand, read_conn

class Monads:
    atom = 0
    char = 1
    complementation = 2
    enclose = 3
    enumerate = 4
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
    amend = 117
    cut = 118
    divide = 119
    drop = 120
    equal = 121
    expand = 122
    find = 123
    form = 141
    format2 = 142
    index = 124
    indexInDepth = 143
    integerDivide = 144
    join = 125
    less = 126
    match = 127
    max = 128
    min = 129
    minus = 130
    more = 131
    plus = 132
    power = 133
    remainder = 135
    reshape = 136
    rotate = 137
    split = 138
    take = 139
    times = 140

    applyMonad = 145
    retype = 146

class Triads:
    applyDyad = 300

class MonadicAdverbs:
    converge = 48
    each = 41
    eachPair = 45
    over = 46
    scanConverging = 53
    scanOver = 51

class DyadicAdverbs:
    each2 = 42
    eachLeft = 43
    eachRight = 44
    overNeutral = 47
    whileOne = 49
    iterate = 50
    scanOverNeutral = 52
    scanWhileOne = 54
    scanIterating = 55

class StorageType:
    WORD = 0
    FLOAT = 1
    WORD_ARRAY = 2 # all integers
    FLOAT_ARRAY = 3 # all floats
    MIXED_ARRAY = 4 # array of storage types

class NounType:
    INTEGER = 10
    REAL = 11
    CHARACTER = 12
    STRING = 13
    LIST = 14
    DICTIONARY = 15
    BUILTIN_SYMBOL = 16
    BUILTIN_MONAD = 17
    BUILTIN_DYAD = 18
    BUILTIN_TRIAD = 19
    MONADIC_ADVERB = 20
    DYADIC_ADVERB = 31
    USER_SYMBOL = 27
    USER_MONAD = 21
    USER_DYAD = 22
    USER_TRIAD = 23
    ERROR = 26
    EXPRESSION = 28
    TYPE = 29
    CONDITIONAL = 30

class SymbolType:
    i = 200
    x = 201
    y = 202
    z = 203
    f = 204
    undefined = 205

class Storage:
    @staticmethod
    def from_conn(conn):
        print('Storage.from_conn')
        data = read_conn(conn)
        print(data)
        return Storage.from_bytes(data)

    @staticmethod
    def from_bytes(data):
        typeBytes = data[0:2]
        untypedData = data[2:]

        (storageType, objectType) = struct.unpack("BB", typeBytes)

        if storageType == StorageType.WORD:
            result, integerRest = Word.from_bytes(untypedData, o=objectType)
            return result, integerRest
        elif storageType == StorageType.FLOAT:
            return Float.from_bytes(untypedData, o=objectType)
        elif storageType == StorageType.WORD_ARRAY:
            result, integerArrayRest = WordArray.from_bytes(untypedData, o=objectType)
            return result, integerArrayRest
        elif storageType == StorageType.FLOAT_ARRAY:
            return FloatArray.from_bytes(untypedData, o=objectType)
        elif storageType == StorageType.MIXED_ARRAY:
            result, mixedArrayRest = MixedArray.from_bytes(untypedData, o=objectType)
            return result, mixedArrayRest

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
        i, rest = expand(data)
        return Word(i, o=o), rest

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
        intBytes = squeeze(self.i)
        return typeBytes + intBytes

class Float(Storage):
    @staticmethod
    def tolerance():
        return 1e-14

    @staticmethod
    def from_bytes(data, o=NounType.REAL):
        i = struct.unpack('d', data)
        return Float(i[0], o=o)

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
        floatBytes = struct.pack("d", self.i)
        data = typeBytes + floatBytes

        length = len(data)
        lengthBytes = squeeze(length)

        return lengthBytes + data

class WordArray(Storage):
    @staticmethod
    def from_bytes(data, o=NounType.LIST):
        rest = data
        results = []
        while len(rest) > 0:
            result, rest = expand(rest)
            results.append(result)
        return WordArray(results, o=o), rest

    def __init__(self, x, o=NounType.LIST):
        super().__init__(o, StorageType.WORD_ARRAY, [int(y) for y in x])

    def __hash__(self):
        return hash((self.o, self.t, self.i))

    def to_conn(self, conn):
        data = self.to_bytes()
        conn.write(data)

    def to_bytes(self):
        typeBytes = struct.pack("BB", self.t, self.o)

        intArrayBytes = b''
        for y in self.i:
            intArrayBytes += squeeze(y)

        data = typeBytes + intArrayBytes

        length = len(data)
        lengthBytes = squeeze(length)

        return lengthBytes + data

class FloatArray(Storage):
    @staticmethod
    def from_bytes(data, o=NounType.LIST):
        rest = data
        results = []
        while len(rest) > 0:
            data = rest[:8]
            rest = rest[8:]

            result = struct.unpack('d', data)[0]
            results.append(result)
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

        floatArrayBytes = b''
        for y in self.i:
            floatArrayBytes += struct.pack("d", y)

        data = typeBytes + floatArrayBytes

        length = len(data)
        lengthBytes = squeeze(length)

        return lengthBytes + data

class MixedArray(Storage):
    @staticmethod
    def from_bytes(data, o=NounType.LIST):
        rest = data
        results = []
        while len(rest) > 0:
            result, rest = Storage.from_bytes(rest)
            results.append(result)
        return MixedArray(results, o=o), rest

    def __init__(self, x, o=NounType.LIST):
        super().__init__(o, StorageType.MIXED_ARRAY, x)

    def __hash__(self):
        return hash((self.o, self.t, self.i))

    def to_conn(self, conn):
        data = self.to_bytes()
        conn.write(data)

    def to_bytes(self):
        typeBytes = struct.pack("BB", self.t, self.o)

        floatArrayBytes = b''
        for y in self.i:
            floatArrayBytes += y.to_bytes()

        data = typeBytes + floatArrayBytes

        length = len(data)
        lengthBytes = squeeze(length)

        return lengthBytes + data
