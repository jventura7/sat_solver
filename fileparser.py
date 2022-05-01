"""
ECE 4524 Project 5
John Ventura
5/1/22
dpll file. This file parses a test txt file and outputs the clauses and symbols
"""

def parse(file):
    """
    This function takes in a txt file and parses it and returns a set of clauses and
    a list of symbols. This is done by reading the file line by line and split the line
    in order to access the symbols.

    :param file: txt file
    :return: set of clauses and list of symbols
    """
    symbolsList = []
    clauses = set()
    with open(file) as f:
        line = f.readline()
        while line:
            # if the line is a comment, skip over it
            if line[0] == 'c':
                line = f.readline()
                continue
            # generate the symbol list
            elif line[0] == 'p':
                _, _, numSymbols, numClauses = line.split(' ')
                symbolsList = [i for i in range(1, int(numSymbols) + 1)]
            # split the clause line and add to clauses set
            else:
                symbols = line.split(' ')
                clause = []
                for symbol in symbols:
                    if symbol.isnumeric() or symbol.lstrip('-').isnumeric():
                        if symbol != '0':
                            clause.append(int(symbol))
                clauses.add(tuple(clause))
            line = f.readline()
    f.close()
    return clauses, symbolsList
