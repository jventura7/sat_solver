from fileparser import parse
from dpll import SATSolver

testfile = 'Project5_testcases/c17.txt'
clauses, symbols = parse(testfile)
solver = SATSolver(clauses, symbols)

if solver.result is True:
    print('DPLL: Satisfied')
else:
    print('DPLL: Not Satisfied')

if solver.model:
    model = []
    for val in solver.model:
        if solver.model[val]:
            model.append('1')
        else:
            model.append('0')
    print('Model:', ''.join(model))
else:
    print('Model: N/A')

print('Calls: ', solver.numCalls)