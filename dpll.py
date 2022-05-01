"""
ECE 4524 Project 5
John Ventura
5/1/22
dpll file. This file creates an SAT solver class which runs the dpll function.
It also contains the helper functions for the dpll algorithm.
"""

class SATSolver:
    """
    Attributes
    ----------
    numCalls : int
        the number of recursive calls made to the dpll function
    model : dict
        the propositional symbols model
    clauses : set
        the set of cnf clauses
    symbols : list
        the list of propositional symbols
    result : boolean
        the result of the sentence

    Methods
    -------
    DPLL(clauses, symbols, model)
        performs the dpll algorithm and determines the sentence result
    """

    def __init__(self, clauses, symbols):
        """
        :param clauses: a set of clauses in the CNF representation of s
        :param symbols: a list of propositional symbols in s
        """
        self.numCalls = 0
        self.model = None
        self.clauses, self.symbols = clauses, symbols
        self.result = self.DPLL(self.clauses, self.symbols, {})

    def DPLL(self, clauses, symbols, model):
        """
        This is the dpll algorithm. It determines if a valid model exists
        in order for early termination, if not the pure symbols and unit clauses
        are found and the function then recursively calls itself.

        :param clauses: a set of clauses in the CNF representation of s
        :param symbols: a list of propositional symbols in s
        :param model: a dictionary containing propositional symbols and a boolean assignment
        :return: a boolean whether the sentence is True or False
        """
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
        rest = symbols.copy()
        P = rest.pop(0)
        modelTrue = model.copy()
        modelFalse = model.copy()
        modelTrue[P] = True
        modelFalse[P] = False
        return self.DPLL(clauses, rest, modelTrue) or self.DPLL(clauses, rest, modelFalse)


def checkEarlyTerminationTrue(clauses, model):
    """
    This function determines if a model exists such that every clause in clauses
    evaluates to True. This is done by keeping a count and checking to see
    if the count is equal to the length of clauses after iterating through
    every clause.

    :param clauses: a set of clauses in the CNF representation of s
    :param model: a dictionary containing propositional symbols and a boolean assignment
    :return: whether every clause in clauses is True
    """
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

def checkEarlyTerminationFalse(clauses, model):
    """
    This function determines if a model exists such that is a clause in clauses
    that evaluates to False. This is done by keeping a count and checking to see
    if the count is equal to the length of a clauses after iterating through every
    literal in the clause.

    :param clauses: a set of clauses in the CNF representation of s
    :param model: a dictionary containing propositional symbols and a boolean assignment
    :return: whether there is a clause in clauses that is False
    """
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
    """
    This function determines if there is a pure symbol in the sentence. A pure
    symbol is a symbol that is strictly negative or strictly positive in every
    clause in the clauses.

    :param symbols: a list of propositional symbols
    :param clauses: a set of clauses in the CNF representation of s
    :param model: a dictionary containing propositional symbols and a boolean assignment
    :return: a pure propositional symbol and the value assigned to it
    """
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
    """
    This function determines if there is a unit clause in clauses. A unit clause
    is a propositional symbol that is the only symbol left in a clause.

    :param clauses: a set of clauses in the CNF representation of s
    :param model: a dictionary containing propositional symbols and a boolean assignment
    :return: a unit propositional symbol and the value assigned to it
    """
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
