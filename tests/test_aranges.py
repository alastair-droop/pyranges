import pytest
import sys
from random import randrange
sys.path.append('../')
from ranges import ARange

# Generate a set of ARanges for testing:
max_len = 100
n_double = 0
n_single = 0

def pytest_generate_tests(metafunc):
    testdata = []
    for i in range(n_double):
        se = sorted([randrange(1, max_len + 1) for i in range(2)])
        r = ARange(se[0], se[1])
        testdata.append((se[0], se[1], list(range(se[0], se[1] + 1)), r))
    for i in range(n_single):
        start = randrange(1, max_len + 1)
        r = ARange(start)
        testdata.append((start, start, [start], r))
    testdata.append((None, None, [], ARange()))
    metafunc.parametrize("start,end,values,r", testdata)

def test_values(start, end, values, r):
    assert r.start == start
    assert r.end == end

def test_length(start, end, values, r):
    assert len(r) == len(values)

def test_list(start, end, values, r):
    assert r.asList() == values

def test_iterator(start, end, values, r):
    range_list = []
    for i in r: range_list.append(i)
    assert range_list == values

def test_equal(start, end, values, r):
    other = ARange(start=start, end=end)
    assert r == other

def test_copy(start, end, values, r):
    other = r.copy()
    assert r == other

def test_span(start, end, values, r):
    other = r.span
    assert r == other

def test_ranges(start, end, values, r):
    assert r.ranges == [r]

def test_empty(start, end, values, r):
    if len(values) == 0: assert r.empty is True
    else: assert r.empty is False
