#!/usr/bin/env python3

import sys
from random import randrange, sample
sys.path.append('../')
from ranges import ARange, SRange, prettyRange
import operator

# A function to return a random number in the range 1-max_len:
def randomIndex(max_len, inc_none=True):
    if inc_none is False: return randrange(1, max_len + 1)
    out = randrange(0, max_len + 1)
    if out == 0: return None
    return out

# A function to create a random ARange:
def randomARange(max_len, inc_none=True):
    return ARange(start=randomIndex(max_len, inc_none), end=randomIndex(max_len, inc_none))

# A function to create a random SRange:
def randomSRange(max_len, inc_none=True):
    if inc_none is True: min_n = 0
    else: min_n = 1
    n = randrange(min_n, max_len + 1)
    return SRange.fromSet(set(sample(range(1, max_len + 1), n)))

# A function to generate a random range (of given type):
def randomRange(rtype, max_len, inc_none=True):
    if rtype == 'A': return randomARange(max_len, inc_none)
    return randomSRange(max_len, inc_none)

# A function to test a binary range function:
def testBinaryFunction(fun, symbol, n, print_ranges=True):
    symbol = str(symbol)
    n_symbol = len(symbol)
    ind_str = '{{}}{} : {{}}'.format(''.join([' ' for i in range(n_symbol)]))
    res_str= 'A{}B: {{}}'.format(symbol)
    for i in range(n):
        # Generate the ranges to test:
        a = randomSRange(max_len)
        b = randomSRange(max_len)
        c = fun(a, b)
        # Print the ranges:
        if print_ranges is True:
            print('')
            print(ind_str.format('A', prettyRange(a, end=max_len)))
            print(ind_str.format('B', prettyRange(b, end=max_len)))
            print(res_str.format(prettyRange(c, end=max_len)))
        # Check that c is correct:
        assert c.asSet() == fun(a.asSet(), b.asSet())

def testBinaryRelation(fun, symbol, n, print_ranges=True):
    symbol = str(symbol)
    n_symbol = len(symbol)
    ind_str = '{{}}{} : {{}}'.format(''.join([' ' for i in range(n_symbol)]))
    res_str= 'A{}B: {{}}'.format(symbol)
    for i in range(n):
        # Generate the ranges to test:
        a = randomSRange(max_len)
        b = randomSRange(max_len)
        res = fun(a, b)
        # Print the ranges:
        if print_ranges is True:
            print('')
            print(ind_str.format('A', prettyRange(a, end=max_len)))
            print(ind_str.format('B', prettyRange(b, end=max_len)))
            print(res_str.format(res))
        # Check that the result is correct:
        assert fun(a.asSet(), b.asSet()) == res

def testLeftOverhang(n, print_ranges=True):
    ind_str = '{}                 : {}'
    res_str = 'leftoverhang(A, B): {}'
    for i in range(n):
        # Generate the ranges to test:
        a = randomSRange(max_len)
        b = randomSRange(max_len)
        c = a.leftOverhang(b)
        # Print the ranges:
        if print_ranges is True:
            print('')
            print(ind_str.format('A', prettyRange(a, end=max_len)))
            print(ind_str.format('B', prettyRange(b, end=max_len)))
            print(res_str.format(prettyRange(c, end=max_len)))
        # Check that the result is correct:
        res = []
        for r in a:
            for i in r:
                if (b.span.start is None) or (i < b.span.start):
                    res.append(i)
        assert(set(res) == c.asSet())

def testRightOverhang(n, print_ranges=True):
    ind_str = '{}                  : {}'
    res_str = 'rightoverhang(A, B): {}'
    for i in range(n):
        # Generate the ranges to test:
        a = randomSRange(max_len)
        b = randomSRange(max_len)
        c = a.rightOverhang(b)
        # Print the ranges:
        if print_ranges is True:
            print('')
            print(ind_str.format('A', prettyRange(a, end=max_len)))
            print(ind_str.format('B', prettyRange(b, end=max_len)))
            print(res_str.format(prettyRange(c, end=max_len)))
        # Check that the result is correct:
        res = []
        for r in a:
            for i in r:
                if (b.span.end is None) or (i > b.span.end):
                    res.append(i)
        assert(set(res) == c.asSet())
        

# Run the tests:
max_len = 25
n_tests = 10000
show = False

binary_functions = {
    '|': operator.__or__,
    '&': operator.__and__,
    '^': operator.__xor__,
    '-': operator.__sub__
}

binary_relations = {
    '==': operator.__eq__,
    '!=': operator.__ne__,
    '<=': operator.__le__,
    '>=': operator.__ge__,
    '<': operator.__lt__,
    '>': operator.__gt__
}

total = 0
for rtype in ['A', 'S']:   
    for i in binary_functions.keys():
        testBinaryFunction(binary_functions[i], i, n_tests, print_ranges=show)
        total += n_tests
    for i in binary_relations.keys():
        testBinaryRelation(binary_relations[i], i, n_tests, print_ranges=show)
        total += n_tests
    testLeftOverhang(n_tests, print_ranges=show)
    total += n_tests
    testRightOverhang(n_tests, print_ranges=show)
    total += n_tests

print('PASSED {} tests'.format(total))
sys.exit(0)
