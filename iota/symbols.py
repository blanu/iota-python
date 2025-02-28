from iota.storage import Monads, Dyads, Triads, MonadicAdverbs, DyadicAdverbs, SymbolType, Word, NounType

# Extension Monads

evaluate = Word(Monads.evaluate, o=NounType.BUILTIN_MONAD)
erase = Word(Monads.erase, o=NounType.BUILTIN_MONAD)
truth = Word(Monads.truth, o=NounType.BUILTIN_MONAD)

# Extension Dyads

applyMonad = Word(Dyads.applyMonad, o=NounType.BUILTIN_DYAD)
retype = Word(Dyads.retype, o=NounType.BUILTIN_DYAD)

# Triads

applyDyad = Word(Triads.applyDyad, o=NounType.BUILTIN_TRIAD)

# Monads

atom = Word(Monads.atom, o=NounType.BUILTIN_MONAD)
char = Word(Monads.char, o=NounType.BUILTIN_MONAD)
inot = Word(Monads.inot, o=NounType.BUILTIN_MONAD)
enclose = Word(Monads.enclose, o=NounType.BUILTIN_MONAD)
ienumerate = Word(Monads.enumerate, o=NounType.BUILTIN_MONAD)
expand = Word(Monads.expand, o=NounType.BUILTIN_MONAD)
first = Word(Monads.first, o=NounType.BUILTIN_MONAD)
floor = Word(Monads.floor, o=NounType.BUILTIN_MONAD)
iformat = Word(Monads.format, o=NounType.BUILTIN_MONAD)
gradeUp = Word(Monads.gradeUp, o=NounType.BUILTIN_MONAD)
gradeDown = Word(Monads.gradeDown, o=NounType.BUILTIN_MONAD)
group = Word(Monads.group, o=NounType.BUILTIN_MONAD)
negate = Word(Monads.negate, o=NounType.BUILTIN_MONAD)
reciprocal = Word(Monads.reciprocal, o=NounType.BUILTIN_MONAD)
reverse = Word(Monads.reverse, o=NounType.BUILTIN_MONAD)
shape = Word(Monads.shape, o=NounType.BUILTIN_MONAD)
size = Word(Monads.size, o=NounType.BUILTIN_MONAD)
transpose = Word(Monads.transpose, o=NounType.BUILTIN_MONAD)
unique = Word(Monads.unique, o=NounType.BUILTIN_MONAD)

# Dyads

amend = Word(Dyads.amend, o=NounType.BUILTIN_DYAD)
cut = Word(Dyads.cut, o=NounType.BUILTIN_DYAD)
divide = Word(Dyads.divide, o=NounType.BUILTIN_DYAD)
drop = Word(Dyads.drop, o=NounType.BUILTIN_DYAD)
equal = Word(Dyads.equal, o=NounType.BUILTIN_DYAD)
find = Word(Dyads.find, o=NounType.BUILTIN_DYAD)
form = Word(Dyads.form, o=NounType.BUILTIN_DYAD)
format2 = Word(Dyads.format2, o=NounType.BUILTIN_DYAD)
index = Word(Dyads.index, o=NounType.BUILTIN_DYAD)
indexInDepth = Word(Dyads.indexInDepth, o=NounType.BUILTIN_DYAD)
integerDivide = Word(Dyads.integerDivide, o=NounType.BUILTIN_DYAD)
join = Word(Dyads.join, o=NounType.BUILTIN_DYAD)
less = Word(Dyads.less, o=NounType.BUILTIN_DYAD)
match = Word(Dyads.match, o=NounType.BUILTIN_DYAD)
imax = Word(Dyads.max, o=NounType.BUILTIN_DYAD)
imin = Word(Dyads.min, o=NounType.BUILTIN_DYAD)
minus = Word(Dyads.minus, o=NounType.BUILTIN_DYAD)
more = Word(Dyads.more, o=NounType.BUILTIN_DYAD)
plus = Word(Dyads.plus, o=NounType.BUILTIN_DYAD)
power = Word(Dyads.power, o=NounType.BUILTIN_DYAD)
remainder = Word(Dyads.remainder, o=NounType.BUILTIN_DYAD)
reshape = Word(Dyads.reshape, o=NounType.BUILTIN_DYAD)
rotate = Word(Dyads.rotate, o=NounType.BUILTIN_DYAD)
split = Word(Dyads.split, o=NounType.BUILTIN_DYAD)
take = Word(Dyads.take, o=NounType.BUILTIN_DYAD)
times = Word(Dyads.times, o=NounType.BUILTIN_DYAD)

# Monadic Adverbs

converge = Word(MonadicAdverbs.converge, o=NounType.MONADIC_ADVERB)
each = Word(MonadicAdverbs.each, o=NounType.MONADIC_ADVERB)
eachPair = Word(MonadicAdverbs.eachPair, o=NounType.MONADIC_ADVERB)
over = Word(MonadicAdverbs.over, o=NounType.MONADIC_ADVERB)
scanConverging = Word(MonadicAdverbs.scanConverging, o=NounType.MONADIC_ADVERB)
scanOver = Word(MonadicAdverbs.scanOver, o=NounType.MONADIC_ADVERB)

# Dyadic Adverbs

each2 = Word(DyadicAdverbs.each2, o=NounType.DYADIC_ADVERB)
eachLeft = Word(DyadicAdverbs.eachLeft, o=NounType.DYADIC_ADVERB)
eachRight = Word(DyadicAdverbs.eachRight, o=NounType.DYADIC_ADVERB)
overNeutral = Word(DyadicAdverbs.overNeutral, o=NounType.DYADIC_ADVERB)
iterate = Word(DyadicAdverbs.iterate, o=NounType.DYADIC_ADVERB)
scanIterating = Word(DyadicAdverbs.scanIterating, o=NounType.DYADIC_ADVERB)
scanOverNeutral = Word(DyadicAdverbs.scanOverNeutral, o=NounType.DYADIC_ADVERB)
scanWhileOne = Word(DyadicAdverbs.scanWhileOne, o=NounType.DYADIC_ADVERB)
whileOne = Word(DyadicAdverbs.whileOne, o=NounType.DYADIC_ADVERB)

# Builtin Words

i = Word(SymbolType.i, o=NounType.BUILTIN_SYMBOL)
x = Word(SymbolType.x, o=NounType.BUILTIN_SYMBOL)
y = Word(SymbolType.y, o=NounType.BUILTIN_SYMBOL)
z = Word(SymbolType.z, o=NounType.BUILTIN_SYMBOL)
f = Word(SymbolType.f, o=NounType.BUILTIN_SYMBOL)

true = 1
false = 0
