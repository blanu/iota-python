from testify import TestCase, assert_equal

from iota.api import *
from iota.error import *
from iota.storage import *
from iota.symbols import *

# These tests just make sure that all of the modules import correctly.
class IotaTests(TestCase):
    def test_api(self):
        assert_equal(Object.from_python(1), Word(1, o=NounType.INTEGER))

    def test_error(self):
        assert_equal(type(ErrorTypes.TEST_ERROR), int)

    def test_storage(self):
        assert_equal(Word(1, o=NounType.INTEGER).i, Word(1, o=NounType.BUILTIN_SYMBOL).i)

    def test_symbols(self):
        assert_equal(atom.i, Monads.atom)

class SqueezeTests(TestCase):
    def test_word(self):
        assert_equal(Storage.from_bytes(Word(0).to_bytes())[0], Word(0))
        assert_equal(Storage.from_bytes(Word(1).to_bytes())[0], Word(1))
        assert_equal(Storage.from_bytes(Word(-1).to_bytes())[0], Word(-1))
        assert_equal(Storage.from_bytes(Word(256).to_bytes())[0], Word(256))
        assert_equal(Storage.from_bytes(Word(-256).to_bytes())[0], Word(-256))

    def test_word_array(self):
        assert_equal(Storage.from_bytes(WordArray([0]).to_bytes())[0], WordArray([0]))
        assert_equal(Storage.from_bytes(WordArray([1]).to_bytes())[0], WordArray([1]))
        assert_equal(Storage.from_bytes(WordArray([-1]).to_bytes())[0], WordArray([-1]))
        assert_equal(Storage.from_bytes(WordArray([256]).to_bytes())[0], WordArray([256]))
        assert_equal(Storage.from_bytes(WordArray([-256]).to_bytes())[0], WordArray([-256]))

        assert_equal(Storage.from_bytes(WordArray([0, 0]).to_bytes())[0], WordArray([0, 0]))
        assert_equal(Storage.from_bytes(WordArray([1, 1]).to_bytes())[0], WordArray([1, 1]))
        assert_equal(Storage.from_bytes(WordArray([-1, -1]).to_bytes())[0], WordArray([-1, -1]))
        assert_equal(Storage.from_bytes(WordArray([256, 256]).to_bytes())[0], WordArray([256, 256]))
        assert_equal(Storage.from_bytes(WordArray([-256, -256]).to_bytes())[0], WordArray([-256, -256]))

        assert_equal(Storage.from_bytes(WordArray([]).to_bytes())[0], WordArray([]))

class EncodeTests(TestCase):
    def test_float(self):
        assert_equal(Storage.from_bytes(Float(0).to_bytes())[0], Float(0))

if __name__ == "__main__":
    # Run tests when executed
    from testify import run

    run()
