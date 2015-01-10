def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [a+b for a in A for b in B]

digits   = '123456789'
rows     = 'ABCDEFGHI'
cols     = digits
squares  = cross(rows, cols)
#squares2  = [cross(r, cols) for r in rows]
unitlist = ([cross(rows, c) for c in cols] +
            [cross(r, cols) for r in rows] +
            [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')])
##print squares
##print squares2
##print unitlist

units = dict((s, [u for u in unitlist if s in u]) 
             for s in squares)
peers = dict((s, set(sum(units[s],[]))-set([s]))
             for s in squares)

def assign(values, s, d):
    """Eliminate all the other values (except d) from values[s] and propagate.
    Return values, except return False if a contradiction is detected."""
    other_values = values[s].replace(d, '')
    if all(eliminate(values, s, d2) for d2 in other_values):
        return values
    else:
        return False

def eliminate(values, s, d):
    """Eliminate d from values[s]; propagate when values or places <= 2.
    Return values, except return False if a contradiction is detected."""
    if d not in values[s]:
        return values ## Already eliminated
    values[s] = values[s].replace(d,'')
    ## (1) If a square s is reduced to one value d2, then eliminate d2 from the peers.
    if len(values[s]) == 0:
        return False ## Contradiction: removed last value
    elif len(values[s]) == 1:
        d2 = values[s]
        if not all(eliminate(values, s2, d2) for s2 in peers[s]):
            return False
    ## (2) If a unit u is reduced to only one place for a value d, then put it there.
    for u in units[s]:
        dplaces = [s for s in u if d in values[s]]
    if len(dplaces) == 0:
        return False ## Contradiction: no place for this value
    elif len(dplaces) == 1:
        # d can only be in one place in unit; assign it there
        if not assign(values, dplaces[0], d):
            return False
    return values

def parse_grid(grid):
    """Convert grid to a dict of possible values, {square: digits}, or
    return False if a contradiction is detected."""
    ## To start, every square can be any digit; then assign values from the grid.
    values = dict((s, digits) for s in squares)
    for s,d in grid_values(grid).items():
        if d in digits and not assign(values, s, d):
            return False ## (Fail if we can't assign d to square s.)
    return values

def grid_values(grid):
    "Convert grid into a dict of {square: char} with '0' or '.' for empties."
    chars = [c for c in grid if c in digits or c in '0.']
    assert len(chars) == 81
    return dict(zip(squares, chars))

def display(values):
    "Display these values as a 2-D grid."
    width = 1+max(len(values[s]) for s in squares)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print ''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols)
        if r in 'CF': print line
    print



def some(seq):
    "Return some element of seq that is true."
    for e in seq:
        if e: return e
    return False

def search(values):
    "Using depth-first search and propagation, try all possible values."
    if values is False:
        return False ## Failed earlier
    if all(len(values[s]) == 1 for s in squares): 
        return values ## Solved!
    ## Chose the unfilled square s with the fewest possibilities
    n,s = min((len(values[s]), s) for s in squares if len(values[s]) > 1)
    return some(search(assign(values.copy(), s, d)) 
		for d in values[s])


##
##
##
## The main contribution starts from here.

def sq_int(pg):
    pg2 = pg
    unitlist = [['A1', 'A2', 'A3', 'B1', 'B2', 'B3', 'C1', 'C2', 'C3'], ['A4', 'A5', 'A6', 'B4', 'B5', 'B6', 'C4', 'C5', 'C6'], ['A7', 'A8', 'A9', 'B7', 'B8', 'B9', 'C7', 'C8', 'C9'], ['D1', 'D2', 'D3', 'E1', 'E2', 'E3', 'F1', 'F2', 'F3'], ['D4', 'D5', 'D6', 'E4', 'E5', 'E6', 'F4', 'F5', 'F6'], ['D7', 'D8', 'D9', 'E7', 'E8', 'E9', 'F7', 'F8', 'F9'], ['G1', 'G2', 'G3', 'H1', 'H2', 'H3', 'I1', 'I2', 'I3'], ['G4', 'G5', 'G6', 'H4', 'H5', 'H6', 'I4', 'I5', 'I6'], ['G7', 'G8', 'G9', 'H7', 'H8', 'H9', 'I7', 'I8', 'I9']]

    ##print unitlist[0]

    for k in range(9):
        a = [pg2[unitlist[k][j]] for j in range(9)]
        r = 0
        c = 0
        rowint = set(a[0]).intersection(a[1]).intersection(a[2]), set(a[3]).intersection(a[4]).intersection(a[5]), set(a[6]).intersection(a[7]).intersection(a[8])

            
##        print rowint
        colint = set(a[0]).intersection(a[3]).intersection(a[6]), set(a[1]).intersection(a[4]).intersection(a[7]), set(a[2]).intersection(a[5]).intersection(a[8])
##        print colint

        for i in range(3):
            if len(rowint[i])!=0:
                r=r+1
            if len(colint[i])!=0:
                c=c+1
        
        if(r!=c or r==0 or c==0):
            continue
##        print k, r, c
        for i in range(9):
            row = rowint[i/3]
            col = colint[i%3]
            
            temp = set(a[i]) - (row&col)

##            print row, col
##            print temp, row&col
##            print
            if(r==2 and r==c):
                if (row.issubset(col) and col.issubset(row) and len(temp)==0):
                    continue
                elif ((row.issubset(col) or col.issubset(row)) and len(row)!=len(col)):
                    continue
            elif len(temp)==0:
                continue
            str1 = ''.join(sorted(temp))
##            print pg2[unitlist[k][i]], str1
            pg2[unitlist[k][i]] = str1
##            print temp
##            print

    return pg


##Baseline
def solve(grid): return search(parse_grid(grid))

##New approach
def solve2(grid): return search(sq_int(parse_grid(grid)))

print 'Start'
grid1 = '52...6.........7.13...........4..8..6......5...........418.........3..2...87.....'

display(parse_grid(grid1))
display(solve(grid1))

time1 = [[0 for i in range(10)] for j in range(10)]
timeb = [[0 for i in range(10)] for j in range(10)]
timen = [[0 for i in range(10)] for j in range(10)]

grid2 = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'

grid3 = '..53.....8......2..7..1.5..4....53...1..7...6..32...8..6.5....9..4....3......97..'

##display(parse_grid(grid2))
import time, random
for iter in range(10):

    pg = parse_grid(grid2)
#print pg

##    pg2 = {'I6': '5789', 'H9': '4689', 'I2': '6789', 'E8': '12359', 'H3': '3', 'H7': '69', 'I7': '23569', 'I4': '589', 'H5': '479', 'F9': '23789', 'G7': '1259', 'G6': '3', 'G5': '459', 'E1': '3679', 'G3': '289', 'G2': '89', 'G1': '289', 'I1': '1', 'C8': '12349', 'I3': '4', 'E5': '8', 'I5': '579', 'C9': '123469', 'G9': '12489', 'G8': '7', 'A1': '4', 'A3': '12679', 'A2': '1679', 'A5': '2369', 'A4': '139', 'A7': '8', 'A6': '269', 'C3': '125689', 'C2': '15689', 'C1': '2689', 'E6': '25679', 'C7': '12369', 'C6': '245689', 'C5': '234569', 'C4': '7', 'I9': '23689', 'D8': '6', 'I8': '23589', 'E4': '359', 'D9': '13789', 'H8': '489', 'F6': '25679', 'A9': '5', 'G4': '6', 'A8': '1239', 'E7': '4', 'E3': '15679', 'F1': '36789', 'F2': '4', 'F3': '56789', 'F4': '359', 'F5': '1', 'E2': '15679', 'F7': '23579', 'F8': '23589', 'D2': '2', 'H1': '5', 'H6': '1', 'H2': '6789', 'H4': '2', 'D3': '15789', 'B4': '14589', 'B5': '24569', 'B6': '245689', 'B7': '12679', 'E9': '12379', 'B1': '26789', 'B2': '3', 'B3': '1256789', 'D6': '4579', 'D7': '13579', 'D4': '3459', 'D5': '34579', 'B8': '1249', 'B9': '124679', 'D1': '3789'}
##pg3 = {'I6': '5789', 'H9': '4689', 'I2': '6789', 'E8': '12359', 'H3': '3', 'H7': '69', 'I7': '23569', 'I4': '589', 'H5': '479', 'F9': '23789', 'G7': '1259', 'G6': '3', 'G5': '459', 'E1': '3679', 'G3': '289', 'G2': '89', 'G1': '289', 'I1': '1', 'C8': '12349', 'I3': '4', 'E5': '8', 'I5': '579', 'C9': '123469', 'G9': '12489', 'G8': '7', 'A1': '4', 'A3': '12679', 'A2': '1679', 'A5': '2369', 'A4': '139', 'A7': '8', 'A6': '269', 'C3': '125689', 'C2': '15689', 'C1': '2689', 'E6': '25679', 'C7': '12369', 'C6': '245689', 'C5': '234569', 'C4': '7', 'I9': '23689', 'D8': '6', 'I8': '23589', 'E4': '359', 'D9': '13789', 'H8': '489', 'F6': '25679', 'A9': '5', 'G4': '6', 'A8': '1239', 'E7': '4', 'E3': '15679', 'F1': '36789', 'F2': '4', 'F3': '56789', 'F4': '359', 'F5': '1', 'E2': '15679', 'F7': '23579', 'F8': '23589', 'D2': '2', 'H1': '5', 'H6': '1', 'H2': '6789', 'H4': '2', 'D3': '15789', 'B4': '14589', 'B5': '24569', 'B6': '245689', 'B7': '12679', 'E9': '12379', 'B1': '26789', 'B2': '3', 'B3': '1256789', 'D6': '4579', 'D7': '13579', 'D4': '3459', 'D5': '34579', 'B8': '1249', 'B9': '124679', 'D1': '3789'}
##pg3 = sq_int(pg3);
##pg2['D4'] = '34'
##pg2['D6'] = '47'
##
##pg2['I5'] = '57'
##
##pg2['C3'] = '1258'
##
##pg2['F9'] = '278'
##
##pg2['B5'] = '2456'
##pg2['B6'] = '24568'


##display(pg2)
##display(pg3)

#print pg2

    solve(grid1)
    start = time.clock()

    solve(grid1)

    t1 = time.clock()-start
    

##    print t

    start = time.clock()

    solve2(grid1)

    t2 = time.clock()-start

    timeb[0][iter] = t1
    timen[0][iter] = t2

    time1[0][iter] = int(100 * (t1-t2)/t1)

##    print timeb[0][iter], timen[0][iter], time1[0][iter]


##    print t1, t2

    

    start = time.clock()

    solve(grid2)

    t1 = time.clock()-start

##    print t

    start = time.clock()

    solve2(grid2)

    t2 = time.clock()-start

    timeb[1][iter] = t1
    timen[1][iter] = t2    
    time1[1][iter] = int(100 * (t1-t2)/t1)
    
##    print t1, t2

##start = time.clock()
##
##display(search(pg3))
##
##t = time.clock()-start
##
##print t


##    pg = parse_grid(grid3)
##    display(pg)
##    pg2 = {'I6': '9', 'H9': '1258', 'I2': '2358', 'E8': '459', 'H3': '4', 'H7': '1268', 'I7': '7', 'I4': '1468', 'H5': '268', 'F9': '1457', 'G7': '1248', 'G6': '12478', 'G5': '2348', 'E1': '259', 'G3': '1278', 'G2': '6', 'G1': '1237', 'I1': '1235', 'C8': '469', 'I3': '128', 'E5': '7', 'I5': '23468', 'C9': '348', 'G9': '9', 'G8': '14', 'A1': '1269', 'A3': '5', 'A2': '249', 'A5': '24689', 'A4': '3', 'A7': '14689', 'A6': '24678', 'C3': '269', 'C2': '7', 'C1': '2369', 'E6': '3', 'C7': '5', 'C6': '2468', 'C5': '1', 'C4': '4689', 'I9': '12458', 'D8': '179', 'I8': '1456', 'E4': '489', 'D9': '127', 'H8': '3', 'F6': '146', 'A9': '1478', 'G4': '5', 'A8': '14679', 'E7': '249', 'E3': '289', 'F1': '5679', 'F2': '59', 'F3': '3', 'F4': '2', 'F5': '469', 'E2': '1', 'F7': '149', 'F8': '8', 'D2': '289', 'H1': '12579', 'H6': '12678', 'H2': '2589', 'H4': '1678', 'D3': '26789', 'B4': '4679', 'B5': '5', 'B6': '467', 'B7': '1469', 'E9': '6', 'B1': '8', 'B2': '349', 'B3': '169', 'D6': '5', 'D7': '3', 'D4': '1689', 'D5': '689', 'B8': '2', 'B9': '1347', 'D1': '4'}
##    pg3 = {'I6': '9', 'H9': '1258', 'I2': '2358', 'E8': '459', 'H3': '4', 'H7': '1268', 'I7': '7', 'I4': '1468', 'H5': '268', 'F9': '1457', 'G7': '1248', 'G6': '12478', 'G5': '2348', 'E1': '259', 'G3': '1278', 'G2': '6', 'G1': '1237', 'I1': '1235', 'C8': '469', 'I3': '128', 'E5': '7', 'I5': '23468', 'C9': '348', 'G9': '9', 'G8': '14', 'A1': '1269', 'A3': '5', 'A2': '249', 'A5': '24689', 'A4': '3', 'A7': '14689', 'A6': '24678', 'C3': '269', 'C2': '7', 'C1': '2369', 'E6': '3', 'C7': '5', 'C6': '2468', 'C5': '1', 'C4': '4689', 'I9': '12458', 'D8': '179', 'I8': '1456', 'E4': '489', 'D9': '127', 'H8': '3', 'F6': '146', 'A9': '1478', 'G4': '5', 'A8': '14679', 'E7': '249', 'E3': '289', 'F1': '5679', 'F2': '59', 'F3': '3', 'F4': '2', 'F5': '469', 'E2': '1', 'F7': '149', 'F8': '8', 'D2': '289', 'H1': '12579', 'H6': '12678', 'H2': '2589', 'H4': '1678', 'D3': '26789', 'B4': '4679', 'B5': '5', 'B6': '467', 'B7': '1469', 'E9': '6', 'B1': '8', 'B2': '349', 'B3': '169', 'D6': '5', 'D7': '3', 'D4': '1689', 'D5': '689', 'B8': '2', 'B9': '1347', 'D1': '4'}
##    pg3 = sq_int(pg3);
##    pg2['A9'] = '178'
##
##    pg2['I1'] = '135'
##
##    pg2['H5'] = '26'

##display(pg2)
##display(pg3)

    start = time.clock()

    solve(grid3)
##display(search(pg))

    t1 = time.clock()-start

##    print t

    start = time.clock()

    solve2(grid3)
##display(search(pg3))

    t2 = time.clock()-start

    timeb[2][iter] = t1
    timen[2][iter] = t2
    time1[2][iter] = int(100 * (t1-t2)/t1)
    print timeb[2][iter], timen[2][iter], time1[2][iter]
##    print t1,t2
##    print

print time1[0]
print time1[1]
print time1[2]





