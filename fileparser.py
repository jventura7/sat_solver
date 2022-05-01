def parse(file):
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