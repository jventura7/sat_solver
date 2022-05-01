"""
ECE 4524 Project 5
John Ventura
5/1/22
Main file. Calls the parsing function, dpll function, and random generation function
When this file is ran, It will run the five test cases and print out their name,
whether it is SAT or NON SAT, the model, and the number of calls, as well as show the graph
from the random test generation.
"""

from fileparser import parse
from dpll import SATSolver
from collections import OrderedDict
from generateRandom import runGraph

def printResults(solved, filename):
    """
    This function prints the results after running the dpll algorothm.

    :param solved: the instance of SATSolver
    :param filename: the name of the test file
    :return: Null
    """
    print('Test case name: ', filename)
    if solved.result is True:
        print('DPLL: Satisfied')
    else:
        print('DPLL: Not Satisfied')

    if solved.model:
        sortedModel = OrderedDict(sorted(solved.model.items()))
        model = []
        for val in sortedModel:
            if solved.model[val]:
                model.append('1')
            else:
                model.append('0')
        print('Model:', ''.join(model))
    else:
        print('Model: N/A')

    print('Calls: ', solved.numCalls)
    print('\n')

def satsolve(file):
    """
    This function parses the file and runs the dpll algorithm
    :param file: txt file
    :return: Null
    """
    clauses, symbols = parse(file)
    solver = SATSolver(clauses, symbols)
    printResults(solver, file)


if __name__ == '__main__':
    testfiles = ['Project5_testcases/c17.txt', 'Project5_testcases/hole6.txt', 'Project5_testcases/testcase1.txt',
                 'Project5_testcases/testcase-aim-50-1_6-yes1-4.txt', 'Project5_testcases/testcase-quinn.txt']
    for testfile in testfiles:
        satsolve(testfile)
    runGraph()
