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
        assert_equal(type(ErrorTypes.TEST_ERROR.value), int)

    def test_storage(self):
        assert_equal(Word(1, o=NounType.INTEGER).i, Word(1, o=NounType.BUILTIN_SYMBOL).i)

    def test_symbols(self):
        assert_equal(atom, Monads.symbol())
