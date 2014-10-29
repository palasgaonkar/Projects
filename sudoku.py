def check(sud):
    zippedsud = zip(*sud)
    boxedsud = []
    for li, line in enumerate(sud):
        for box in range(3):
            if not li % 3:
                boxedsud.append([])    # build a new box every 3 lines
            boxedsud[box + li / 3 * 3].extend(line[box * 3:box * 3 + 3])

    for li in range(9):
        if [x for x in [set(sud[li]), set(zippedsud[li]), set(boxedsud[li])] if x != set(range(1, 10))]:
            return 'Invalid'
    return 'Valid'


sudoku = [[7, 5, 1, 8, 4, 3, 9, 2, 6],
          [8, 9, 3, 6, 2, 5, 1, 7, 4],
          [6, 4, 2, 1, 7, 9, 5, 8, 3],
          [4, 2, 5, 3, 1, 6, 7, 9, 8],
          [1, 7, 6, 9, 8, 2, 3, 4, 5],
          [9, 3, 8, 7, 5, 4, 6, 1, 2],
          [3, 6, 4, 2, 9, 7, 8, 5, 1],
          [2, 8, 9, 5, 3, 1, 4, 6, 7],
          [5, 1, 7, 4, 6, 8, 2, 3, 9]]

print check(sudoku)

