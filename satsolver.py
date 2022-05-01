from fileparser import parse
from dpll import SATSolver

def printResults(solved):
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

def satsolve(file):
    clauses, symbols = parse(file)
    solver = SATSolver(clauses, symbols)
    printResults(solver)


testfile = 'Project5_testcases/c17.txt'
satsolve(testfile)
