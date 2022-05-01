from fileparser import parse

def checkEarlyTerminationTrue(clauses, model):
    count = 0
    # removed = set()
    for clause in clauses:
        if type(clause) is int:
            clause = set([clause])
        for value in clause:
            if abs(value) in model:
                if value < 0 and not model[abs(value)]:
                    count += 1
                    # removed.add(clause)
                    break
                elif value > 0 and model[abs(value)]:
                    count += 1
                    # removed.add(clause)
                    break
    # for clause in removed:
    #     clauses.remove(clause)
    if count == len(clauses): return True
    return False

def checkEarlyTerminationFalse(clauses, model):
    for clause in clauses:
        count = 0
        if type(clause) is int:
            clause = set([clause])
        for value in clause:
            if abs(value) in model:
                if value < 0 and model[abs(value)]:
                    count += 1
                elif value > 0 and not model[abs(value)]:
                    count += 1
        if count == len(clause): return True
    return False

def findPureSymbol(symbols, clauses, model):
    # 1. remove all clauses which are already true
    newClauses = clauses.copy()
    removed = set()
    for clause in clauses:
        if type(clause) is int:
            clause = set([clause])
        for value in clause:
            if abs(value) in model:
                if value < 0 and not model[abs(value)]:
                    removed.add(clause)
                    break
                elif value > 0 and model[abs(value)]:
                    removed.add(clause)
                    break

    for clause in removed:
        newClauses.remove(clause)

    # 2. loop through symbols and try to find the first pure symbol
    for symbol in symbols:
        numPositives = 0
        numNegatives = 0
        for clause in newClauses:
            if symbol not in clause and -1 * symbol not in clause:
                continue
            if symbol in clause:
                numPositives += 1
            if -1 * symbol in clause:
                numNegatives += 1
        if numNegatives == 0 and numPositives > 0:
            return symbol, True
        elif numNegatives > 0 and numPositives == 0:
            return symbol, False
    return None, None

def findUnitClause(clauses, model):
    # 1. Loop through each clause
    for clause in clauses:
        # 2. If clause is just one literal, return it and its value
        if type(clause) is int:
            if clause > 0:
                return clause, True
            else:
                return -1 * clause, False
        else:
            # 3. If clause is more than one literal, loop through entire clause
            # and check to see if every literal but one is already false. If condition is met,
            # then return the one unassigned symbol and its sign to make clause true
            numNegatives = 0
            numPositives = 0
            notAssigned = None
            for symbol in clause:
                if symbol not in model and -1 * symbol not in model:
                    notAssigned = symbol
                    continue

                if symbol in model:
                    if model[symbol]: numPositives += 1
                    if not model[symbol]: numNegatives += 1

                if -1 * symbol in model:
                    if model[-1 * symbol]: numNegatives += 1
                    if not model[-1 * symbol]: numPositives += 1

            if numNegatives == len(clause) - 1 and numPositives == 0:
                if notAssigned < 0:
                    return -1 * notAssigned, False
                else:
                    return notAssigned, True
    return None, None

class SATSolver:
    def __init__(self, clauses, symbols):
        self.numCalls = 0
        self.model = None
        self.clauses, self.symbols = clauses, symbols
        self.result = self.DPLL(self.clauses, self.symbols, {})

    def DPLL(self, clauses, symbols, model):
        self.numCalls += 1
        if checkEarlyTerminationTrue(clauses, model):
            self.model = model
            return True
        if checkEarlyTerminationFalse(clauses, model):
            return False
        P, value = findPureSymbol(symbols, clauses, model)
        if P:
            temp = symbols.copy()
            temp.remove(P)
            model[P] = value
            return self.DPLL(clauses, temp, model)
        P, value = findUnitClause(clauses, model)
        if P:
            temp = symbols.copy()
            temp.remove(P)
            model[P] = value
            return self.DPLL(clauses, temp, model)
        copyList = symbols.copy()
        P = copyList.pop(0)
        modelTrue = model.copy()
        modelFalse = model.copy()
        modelTrue[P] = True
        modelFalse[P] = False
        return self.DPLL(clauses, copyList, modelTrue) or self.DPLL(clauses, copyList, modelFalse)


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