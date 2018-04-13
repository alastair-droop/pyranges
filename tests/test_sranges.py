import pytest
import sys
from random import randrange, sample
sys.path.append('../')
from ranges import SRange

# Generate a set of ARanges for testing:
max_len = 100
n_tests = 1

def randomSRange(max_len):
    return SRange.fromSet(set(sample(range(1, max_len + 1), randrange(0, max_len + 1))))
    
def pytest_generate_tests(metafunc):
    testdata = []
    for i in range(n_tests):
        testdata.append((randomSRange(max_len), randomSRange(max_len)))
    metafunc.parametrize("r1,r2", testdata)

def test_eq(r1, r2): assert (r1 == r2) == (r1.asSet() == r2.asSet())
def test_le(r1, r2): assert (r1 <= r2) == (r1.asSet() <= r2.asSet())
def test_lt(r1, r2): assert (r1 < r2) == (r1.asSet() < r2.asSet())
def test_ge(r1, r2): assert (r1 >= r2) == (r1.asSet() >= r2.asSet())
def test_gt(r1, r2): assert (r1 > r2) == (r1.asSet() > r2.asSet())

def test_and(r1, r2): assert (r1 & r2).asSet() == (r1.asSet() & r2.asSet())
def test_or(r1, r2): assert (r1 | r2).asSet() == (r1.asSet() | r2.asSet())
def test_sub(r1, r2): assert (r1 - r2).asSet() == (r1.asSet() - r2.asSet())
def test_xor(r1, r2): assert (r1 ^ r2).asSet() == (r1.asSet() ^ r2.asSet())




# def test_copy(values, r):
#     other = r.copy()
#     assert r == other
#
# def test_empty(values, r):
#     if len(values) == 0: assert r.empty is True
#     else: assert r.empty is False
#
