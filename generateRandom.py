"""
ECE 4524 Project 5
John Ventura
5/1/22
random test generation file. This file creates 80 random tests with 50 symbols and up to
400 clauses per test. It then plots the results as a graph of runtime vs. ratio.
"""

import random
import matplotlib.pyplot as plt
from dpll import SATSolver

def generateRandomTests(n, k, numSentences):
    """
    This function constructs a dictionary that represents all our randomly generated test cases.

    :param n: the number of symbols in the sentence
    :param k: the number of literals in a clause
    :param numSentences: the number of test cases
    :return: a dictionary in range of numSentences that contains the set of clauses and list of symbols
    """
    sentences = {i: (set(), [j for j in range(1, n + 1)]) for i in range(1, numSentences + 1)}
    allowedValues = list(range(-50, 51))
    allowedValues.remove(0)
    for sentence in sentences:
        m = random.randint(50, 400)
        for i in range(m):
            sentences[sentence][0].add(tuple(random.sample(allowedValues, k)))
    return sentences

def solve(tests):
    """
    This function will run the dpll algorithm on each of the test cases and then construct
    the plot.

    :param tests: the dict of test cases
    :return: Null
    """
    x, y = [], []
    for test in tests:
        clauses, symbols = tests[test]
        solver = SATSolver(clauses, symbols)
        x.append(len(clauses) / len(symbols))
        y.append(solver.numCalls)

    plt.plot(x, y, 'ro')
    plt.xlabel("Ratio (clauses/symbols)")
    plt.ylabel("Runtime (number of calls)")
    plt.show()

def runGraph():
    """
    This function constructs the randomly generated test cases and then runs dpll on allof them.
    It will then plot the graph of num calls vs. ratio.

    :return: Null
    """
    testcases = generateRandomTests(50, 3, 80)
    solve(testcases)

