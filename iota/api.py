from iota.storage import *
from iota.error import *

def F(*i):
    return Object.from_python_to_expression(list(i))

def C(i):
    if len(i) == 1:
        utf32 = i.encode("utf-32be")
        x = int.from_bytes(utf32, 'big')
        return Word(x, o=NounType.CHARACTER)
    else:
        raise Exception('invalid character')

def QuotedSymbol(i):
    if(i[0] == ':'):
        i = i[1:]

    result = []
    for y in i:
        utf32 = y.encode("utf-32be")
        integer = int.from_bytes(utf32, 'big')
        result.append(integer)

    return WordArray(result, o=NounType.QUOTED_SYMBOL)

def Symbol(i):
    if(i[0] == ':'):
        i = i[1:]

    if i == "x":
        return Word(SymbolType.x, o=NounType.BUILTIN_SYMBOL)
    elif i == "y":
        return Word(SymbolType.y, o=NounType.BUILTIN_SYMBOL)
    elif i == "z":
        return Word(SymbolType.z, o=NounType.BUILTIN_SYMBOL)
    elif i == "f":
        return Word(SymbolType.f, o=NounType.BUILTIN_SYMBOL)
    elif i == "undefined":
        return Word(SymbolType.undefined, o=NounType.BUILTIN_SYMBOL)
    else:
        result = []
        for y in i:
            utf32 = y.encode("utf-32be")
            integer = int.from_bytes(utf32, 'big')
            result.append(integer)

        return WordArray(result, o=NounType.USER_SYMBOL)

class Object:
    @staticmethod
    def from_python(i):
        if type(i) == int:
            return Word(i, o=NounType.INTEGER)
        elif type(i) == float:
            return Float(i, o=NounType.REAL)
        elif type(i) == list:
            if all([type(y) == int for y in i]):
                return WordArray(i, o=NounType.LIST)
            elif all([type(y) == float for y in i]):
                return FloatArray(i, o=NounType.LIST)
            else:
                return MixedArray([Object.from_python(y) for y in i], o=NounType.LIST)
        elif type(i) == tuple:
            return Function.new([Object.from_python(y) for y in list(i)])
        elif type(i) == str:
            utf32 = i.encode("utf-32be")
            ints = [int.from_bytes(utf32[y:y+4], 'big') for y in range(0, len(utf32), 4)]
            return WordArray(ints, o=NounType.STRING)
        elif type(i) == dict:
            keys = [Object.from_python(key) for key in i.keys()]
            values = [Object.from_python(value) for value in i.values()]
            zipped = [Object.from_python(pair) for pair in zip(keys, values)]
            return MixedArray(zipped, o=NounType.DICTIONARY)
        elif isinstance(i, Storage):
            return i

    @staticmethod
    def from_python_to_expression(i):
        parts = [Object.from_python(y) for y in i]
        return Function.new(parts)

    @staticmethod
    def from_bytes(d):
        return Storage.from_bytes(d)

    @staticmethod
    def to_python(i):
        if i.o == NounType.INTEGER:
            return i.i
        elif i.o == NounType.REAL:
            return i.i
        elif i.o == NounType.LIST:
            if i.t == StorageType.WORD_ARRAY:
                return i.i
            elif i.t == StorageType.FLOAT_ARRAY:
                return i.i
            elif i.t == StorageType.MIXED_ARRAY:
                return [Object.to_python(y) for y in i.i]
        elif i.o == NounType.CHARACTER:
            b = int.to_bytes(i.i, 4, 'big')
            return b.decode("utf-32be")
        elif i.o == NounType.STRING:
            b = b''.join([int.to_bytes(y, 4, 'big') for y in i.i])
            return b.decode("utf-32be")
        elif i.o == NounType.DICTIONARY:
            results = {}
            for pair in i.i:
                key = Object.to_python(pair.i[0])
                value = Object.to_python(pair.i[1])
                results[key] = value
            return results
        elif i.o == NounType.BUILTIN_SYMBOL:
            if i.i == SymbolType.x:
                return ":x"
            elif i.i == SymbolType.y:
                return ":y"
            elif i.i == SymbolType.z:
                return ":z"
            elif i.i == SymbolType.f:
                return ":f"
            elif i.i == SymbolType.undefined:
                return ":undefined"
        elif i.o == NounType.USER_SYMBOL:
            results = ":"
            for y in i.i:
                b = int.to_bytes(y, 4, 'big')
                c = b.decode("utf-32be")
                results += c
            return results
        elif i.o == NounType.QUOTED_SYMBOL:
            results = ":"
            for y in i.i:
                b = int.to_bytes(y, 4, 'big')
                c = b.decode("utf-32be")
                results += c
            return results
        elif i.o == NounType.USER_MONAD:
            return None # FIXME
        elif i.o == NounType.USER_DYAD:
            return None # FIXME
        elif i.o == NounType.USER_TRIAD:
            return None # FIXME
        elif i.o == NounType.EXPRESSION:
            return tuple([Object.to_python(y) for y in i.i])
        elif i.o == NounType.ERROR:
            s = error_to_string(i.i)
            raise Exception(s)

class Function(Object):
    @staticmethod
    def checkSymbols(i):
        hasI = False
        hasX = False
        hasY = False
        for y in i:
            if y.o == NounType.INTEGER:
                continue
            elif y.o == NounType.REAL:
                continue
            elif y.o == NounType.LIST:
                if y.t == StorageType.WORD_ARRAY:
                    continue
                elif y.t == StorageType.FLOAT_ARRAY:
                    continue
                elif y.t == StorageType.MIXED_ARRAY:
                    (subHasI, subHasX, subHasY) = Function.checkSymbols(y.i)
                    hasI = hasI or subHasI
                    hasX = hasX or subHasX
                    hasY = hasY or subHasY
            elif y.o == NounType.EXPRESSION:
                (subHasI, subHasX, subHasY) = Function.checkSymbols(y.i)
                hasI = hasI or subHasI
                hasX = hasX or subHasX
                hasY = hasY or subHasY
            else:
                if y.o == NounType.BUILTIN_SYMBOL:
                    if y.i == SymbolType.i:
                        hasI = True
                    if y.i == SymbolType.x:
                        hasX = True
                    if y.i == SymbolType.y:
                        hasY = True
        return hasI, hasX, hasY

    @staticmethod
    def new(i):
        (hasI, hasX, hasY) = Function.checkSymbols(i)
        if hasY:
            return MixedArray(i, o=NounType.USER_TRIAD)
        elif hasX:
            return MixedArray(i, o=NounType.USER_DYAD)
        elif hasI:
            return MixedArray(i, o=NounType.USER_MONAD)
        else:
            return MixedArray(i, o=NounType.EXPRESSION)

def test_error():
    return Word(ErrorTypes.TEST_ERROR, o=NounType.ERROR)

def error_to_string(i):
    if i == ErrorTypes.UNSUPPORTED_SUBJECT:
        return "unsupported subject type"
    elif i == ErrorTypes.TEST_ERROR:
        return "test error"
    elif i == ErrorTypes.INVALID_ARGUMENT:
        return "invalid argument type"
    elif i == ErrorTypes.BAD_INITIALIZATION:
        return "bad initialization value"
    elif i == ErrorTypes.UNSUPPORTED_OBJECT:
        return "operation is not supported by this object type"
    elif i == ErrorTypes.BAD_STORAGE:
        return "this object type does not support this storage type"
    elif i == ErrorTypes.BAD_OPERATION:
        return "this operation is not supported by this object type with this storage type"
    elif i == ErrorTypes.UNKNOWN_KEY:
        return "unknown key"
    elif i == ErrorTypes.INVALID_ADVERB_ARGUMENT:
        return "invalid adverb argument"
    elif i == ErrorTypes.EMPTY:
        return "empty"
    elif i == ErrorTypes.OUT_OF_BOUNDS:
        return "out of bounds"
    elif i == ErrorTypes.UNEQUAL_ARRAY_LENGTHS:
        return "unequal array lengths"
    elif i == ErrorTypes.BAD_INDEX_TYPE:
        return "unsupported index type"
    elif i == ErrorTypes.SHAPE_MISMATCH:
        return "mismatched shapes"
