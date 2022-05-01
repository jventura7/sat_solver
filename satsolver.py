from fileparser import parse
from dpll import SATSolver

def printResults(solved, filename):
    print('Test case name: ', filename)
    if solved.result is True:
        print('DPLL: Satisfied')
    else:
        print('DPLL: Not Satisfied')

    if solved.model:
        model = []
        for val in solved.model:
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
    clauses, symbols = parse(file)
    solver = SATSolver(clauses, symbols)
    printResults(solver, file)


if __name__ == '__main__':
    testfiles = ['Project5_testcases/c17.txt', 'Project5_testcases/hole6.txt', 'Project5_testcases/testcase1.txt',
                 'Project5_testcases/testcase-aim-50-1_6-yes1-4.txt', 'Project5_testcases/testcase-quinn.txt']
    for file in testfiles:
        satsolve(file)