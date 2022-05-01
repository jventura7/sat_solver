import random
import matplotlib.pyplot as plt
from dpll import SATSolver

def generateRandomTests():
    n = 50
    k = 3
    numSentences = 60
    sentences = {i: (set(), [j for j in range(1, n + 1)]) for i in range(1, numSentences + 1)}
    allowedValues = list(range(-50, 51))
    allowedValues.remove(0)
    for sentence in sentences:
        m = random.randint(30, 400)
        for i in range(m):
            sentences[sentence][0].add(tuple(random.sample(allowedValues, k)))
    return sentences

def solve(tests):
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


testcases = generateRandomTests()
solve(testcases)

