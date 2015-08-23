# -*- coding: utf-8 -*-
"""
    factoradic.py
    ~~~~~~~~~~~~~

    Determine nth lexicographic permutation using
    factorial-base number system. See this article:
    https://en.wikipedia.org/wiki/Factorial_number_system#Examples

"""
def get_factorials(n):
    """Memoized sequence of factorials to save calculations."""
    facts = [1] * (n + 1)
    for i in range(1, n + 1):
        facts[i] = i * facts[i - 1]
    return facts

def nth_permutation(array_to_permute, n):
    """Return nth permutation of an array."""
    if not array_to_permute: return None

    A = array_to_permute[:]
    num_choices = len(A)
    ret = [None] * num_choices

    facts = get_factorials(num_choices)

    #: Permutations cycle after factorial(num_choices)
    #: I.e. after "321" comes "123"
    n %= facts[num_choices]

    for i in xrange(num_choices - 1, -1, -1):
        idx, n = divmod(n, facts[i])
        ret[num_choices - i - 1] = A.pop(idx)
    return "".join([str(_) for _ in ret])




"""
    Testing
"""
import unittest
import random
import timeit
import itertools
import sys
class TestPermutations(unittest.TestCase):

    def test_large(self):
        A = range(10 ** 3)
        idx = random.randint(0, 10 ** 3)
        nth_factoradic = nth_permutation(A, idx)
        nth_std_library = nth(itertools.permutations(A), idx)
        nth_std_library = "".join([str(_) for _ in nth_std_library])
        self.assertEqual(nth_factoradic, nth_std_library)

    def test_null(self):
        A = []
        nth_factoradic = nth_permutation(A, 3)
        self.assertEqual(nth_factoradic, None)
  
    def test_specific_values(self):
        nth_factoradic = nth_permutation([1, 2, 3], 3)
        self.assertEqual(nth_factoradic, '231')

        nth_factoradic = nth_permutation(['a', 'b', 'c', 'd'], 2)
        self.assertEqual(nth_factoradic, 'acbd')

        nth_factoradic = nth_permutation(range(10), 999999)
        self.assertEqual(nth_factoradic, '2783915460')

    def runTest(self):
        tests_to_run = ['test_large', 'test_null', 'test_specific_values']
        test_suite = unittest.TestSuite(map(TestPermutations, tests_to_run))
        unittest.TextTestRunner(verbosity=5).run(test_suite)


def nth(iterable, n, default=None):
    """Returns the nth item or a default value"""
    return next(itertools.islice(iterable, n, None), default)

if  __name__ == "__main__":
    print "\n\n"
    print "*" + "-" * 78 + "*"
    print "*" + "TESTS".center(78) + "*"
    print "*" + ("Filename: " + sys.argv[0]).center(78) + "*"
    print "*" + "-" * 78 + "*"
    print "*" + "Sanity checks".center(78) + "*"
    print "*" + "-" * 78 + "*"

    print "Millionth permutation of 0-9: " + nth_permutation(range(10), 999999) 
    print "4th permutation [1,2,3]: " + nth_permutation([1, 2, 3], 3)
    print "4th permutation [-1,-2,-3]: " + nth_permutation([-1, -2, -3], 3)
    print "3rd permutation [a-d]: " + nth_permutation(['a', 'b', 'c', 'd'], 2)
    print "\n"

    print "*" + "-" * 78 + "*"
    print "*" + "Unit tests".center(78) + "*"
    print "*" + "-" * 78 + "*"
    TestPermutations().runTest()
    print "\n"

    print "*" + "-" * 78 + "*"
    print "*" + "Performance statistics".center(78) + "*"
    print "*" + "-" * 78 + "*"
    
    test = timeit.Timer('nth_permutation(range(10 ** 3), 10 ** 3)',
                        setup="from __main__ import nth_permutation")
    print "10 calls, avg time factoradic approach: ", test.timeit(10) / 10.0
    
    # itertools still faster
    test = timeit.Timer('nth(itertools.permutations(range(10 ** 3)), 10 ** 3)',
                        setup="import itertools; from __main__ import nth")
    print "10 calls, avg time itertools function: ", test.timeit(10) / 10.0
    print "*" + "-" * 78 + "*"
