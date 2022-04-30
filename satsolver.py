def getClausesAndSymbols(file):
    symbolsList = []
    clauses = set()
    with open(file) as f:
        line = f.readline()
        while line:
            if line[0] == 'c':
                line = f.readline()
                continue
            elif line[0] == 'p':
                _, _, numSymbols, numClauses = line.split(' ')
                symbolsList = [i for i in range(1, int(numSymbols) + 1)]
            else:
                symbols = line.split(' ')
                clause = []
                for symbol in symbols:
                    if symbol.isnumeric() or symbol.lstrip('-').isnumeric():
                        if symbol != '0':
                            clause.append(int(symbol))
                clauses.add(tuple(clause))
            line = f.readline()

    return clauses, symbolsList

class SATSolver:
    def __init__(self, file):
        self.file = file
        self.numCalls = 0
        self.clauses, self.symbols = getClausesAndSymbols(file)
        self.result, self.model = self.DPLL(self.clauses, self.symbols, {})

    def checkEarlyTerminationTrue(self, clauses, model):
        count = 0
        for clause in clauses:
            if type(clause) is int:
                clause = set([clause])
            for value in clause:
                if abs(value) in model:
                    if value < 0 and not model[abs(value)]:
                        count += 1
                        break
                    elif value > 0 and model[abs(value)]:
                        count += 1
                        break
        if count == len(clauses): return True
        return False

    def checkEarlyTerminationFalse(self, clauses, model):
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

    def findPureSymbol(self, symbols, clauses, model):
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
                if symbol not in clause and -1 * symbol not in clause: continue
                if symbol in clause: numPositives += 1
                if -1 * symbol in clause: numNegatives += 1
            if numNegatives == 0 and numPositives > 0:
                return symbol, True
            elif numNegatives > 0 and numPositives == 0:
                return symbol, False
        return None, None

    def findUnitClause(self, clauses, model):
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
                        if model[symbol]:
                            numPositives += 1
                            # continue
                        if not model[symbol]: numNegatives += 1
                    if -1 * symbol in model:
                        if model[-1 * symbol]: numNegatives += 1
                        if not model[-1 * symbol]:
                            numPositives += 1
                            # continue
                if numNegatives == len(clause) - 1 and numPositives == 0:
                    if notAssigned < 0:
                        return -1 * notAssigned, False
                    else:
                        return notAssigned, True
        return None, None

    def DPLL(self, clauses, symbols, model):
        self.numCalls += 1
        if self.checkEarlyTerminationTrue(clauses, model): return True, model
        if self.checkEarlyTerminationFalse(clauses, model): return False, model
        P, value = self.findPureSymbol(symbols, clauses, model)
        if P:
            temp = symbols.copy()
            temp.remove(P)
            tempModel = model.copy()
            tempModel[P] = value
            return self.DPLL(clauses, temp, tempModel)
        P, value = self.findUnitClause(clauses, model)
        if P:
            temp = symbols.copy()
            temp.remove(P)
            tempModel = model.copy()
            tempModel[P] = value
            return self.DPLL(clauses, temp, tempModel)
        copyList = symbols.copy()
        P = copyList.pop(0)
        modelTrue = model.copy()
        modelFalse = model.copy()
        modelTrue[P] = True
        modelFalse[P] = False
        return self.DPLL(clauses, copyList, modelTrue) or self.DPLL(clauses, copyList, modelFalse)


testfile = 'Project5_testcases/dubois21.txt'
solver = SATSolver(testfile)
print(solver.result, solver.model, solver.numCalls)