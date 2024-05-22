n = int(input("n: "))

def generate_spiral_matrix(n):
    solution = [[0 for i in range(n)] for i in range(n)]
    colum = 0
    row = 0
    direction = 1
    i = 1
    while i < n**2:
        adding = True
        solution[row][colum] = i
        if direction == 0:
            row -= 1
            if row < 0 or solution[row][colum] != 0:
                row += 1
                direction += 1
                adding = False
        elif direction == 1:
            colum += 1
            if colum > n - 1 or solution[row][colum] != 0:
                colum -= 1
                direction += 1
                adding = False
        elif direction == 2:
            row += 1
            if row > n - 1 or solution[row][colum] != 0:
                row -= 1
                direction += 1
                adding = False
        elif direction == 3:
            colum -= 1
            if colum < 0 or solution[row][colum] != 0:
                colum += 1
                direction += 1
                adding = False
        else:
            print("error")
            return
        direction %= 4
        
        if adding:
            i += 1

        print(f"direction: {direction} i: {i}")

    if direction == 0:
        row -= 1
    if direction == 1:
        colum += 1
    if direction == 0:
        row += 1
    if direction == 1:
        colum -= 1

    solution[row][colum] = n**2
    
    #readable printing
    nums = len(str(n**2))
    printlines = ["" for _ in range(n)]
    for i,row in enumerate(solution):
        prstr = ""
        for num in row:
            whitespace = ""
            for _ in range(nums - len(str(num))):
                whitespace += " "
            prstr += whitespace + str(num) + " "
        printlines[i] = prstr

    for row in printlines:
        print(row)

generate_spiral_matrix(n)