from itertools import count
from itertools import cycle
from random import randint
from time import sleep
import sys

p1Board = []
p2Board = []
xLine = []
yLine = []
p1Ships_Sunk = 0
p2Ships_Sunk = 0
ship_Size = [1,2,3]
ship_Axis = ["Hor","Ver"]
p = cycle([1,2])
p1 = 1
p2 = 2
start = stop = None
step = -1
reverse_Slice = slice(start, stop, step)

for x in "Let's play Battleship!\n":
    print (x, end="")
    sys.stdout.flush()
    sleep(0.05)

while True:
    try:
        sleep(1)
        size = int(input("Please enter the size of the battle zone: "))
    except ValueError:
        print ("Sorry! The input you entered must be an integer.")
        continue
    else:
        if size <= 0:
            print ("Your size cannot be less than or equal to 0.")
            continue
        break

while True:
    try:
        sleep(1)
        ship_Num = int(input("Please enter the number of battleships: "))
    except ValueError:
        print ("Sorry! The number you entered must be a whole number.")
        continue
    else:
        if ship_Num  > size / 2:
            print ("Sorry! Your number must be less than or equal to half the size of the battle zone.")
            continue
        elif ship_Num <= 0:
            print ("Your number must be greater than and not equal to 0.")
            continue
        else:
            sleep(1)
            break

for x in range(size-1, -1, -1):
    xLine.append(str(x))
    yLine.append(str(x))
yLine.sort()

for x in range(size):
    p1Board.append(["O"] * size)
p1Board.reverse()
for x in range(size):
    p2Board.append(["O"] * size)
p2Board.reverse()

def print_board(p1Board, xLine, yLine):
    v = 0
    for row in p1Board[reverse_Slice]:
        print (" ", xLine[v], " ", " ".join(row))
        v += 1
    print ("")
    print ("     ", end=" ")
    for num in yLine:
        print (num, end=" ")
    print ("")

def size2(ship_x, ship_y, c, size, t, n, b):
    ship_x.extend(([[n, n+1]]))
    ship_y.append(b)
    while c < len(ship_x[t]):
        if ship_x[t][c] >= size:
            ship_x[t].remove(ship_x[t][c])
            if len(ship_x[t]) == 1:
                ship_x[t] = int(ship_x[t][0])
            c = 1
            break
        c += 1

def size3(ship_x, ship_y, c, size, t, n, b):
    ship_x.extend(([[n, n+1, n+2]]))
    ship_y.append(b)
    while c < len(ship_x[t]):
        if ship_x[t][c] >= size:
            ship_x[t].remove(ship_x[t][c])
            if len(ship_x[t]) == 1:
                ship_x[t] = int(ship_x[t][0])
                break
            continue
        c += 1

def remove_Duplicates(ship_x, c, size, t):
    if not isinstance(ship_x[t], int):
        if len(ship_x[t]) == 2:
            if ship_x[t][c] in ship_x:
                ship_x[t].remove(ship_x[t][c])
        else:
            for v in range(2,0,-1):
                if ship_x[t][v] in ship_x:
                    ship_x[t].remove(ship_x[t][v])

def ships(p1Board, ship_Num, ship_Size, size):
    ship_x = []
    ship_y = []
    ship_row = []
    ship_col = []
    for x in range(ship_Num):
        ship_row.append(randint(0, len(p1Board[0])-1)); ship_col.append(randint(0, len(p1Board)-1))
        ship_row = list(set(ship_row)); ship_col = list(set(ship_col))
    for c in count():
        if len(ship_row) < ship_Num:
            ship_row.append(randint(0, len(p1Board)-1))
            ship_row = list(set(ship_row))
        else:
            break
    for v in count():
        if len(ship_col) < ship_Num:
            ship_col.append(randint(0, len(p1Board[0])-1))
            ship_col = list(set(ship_col))
        else:
            break
    for t in range(0, ship_Num):
        axis = ship_Axis[randint(0,1)]
        c = 1
        n = ship_row[t]
        b = ship_col[t]
        f = randint(1, len(ship_Size))
        if f == 1:
            ship_x.append(n); ship_y.append(b)
            continue
        elif f == 2:
            if axis == "Ver":
                size2(ship_x, ship_y, c, size, t, n, b)
                continue
            elif axis == "Hor":
                size2(ship_y, ship_x, c, size, t, b, n)
                continue
        else:
            if axis == "Ver":
                size3(ship_x, ship_y, c, size, t, n, b)
                continue
            elif axis == "Hor":
                size3(ship_y, ship_x, c, size, t, b, n)
                continue
    for t in range(0, ship_Num):
        remove_Duplicates(ship_x, c, size, t)
        remove_Duplicates(ship_y, c, size, t)
    return ship_x, ship_y

p1Ship_x, p1Ship_y = ships(p1Board, ship_Num, ship_Size, size)
p2Ship_x, p2Ship_y = ships(p2Board, ship_Num, ship_Size, size)
p1shots = ship_Num * 4
p2shots = ship_Num * 4

def ship_loc(p1Board, p1Ship_x, p1Ship_y):
    sleep(1)
    print ("These were the locations of the remaining ships (shown with the letter 'S'): ")
    print (" ")
    sleep(1)
    for x in range(0, len(p1Ship_x)):
        try:
            p1Board[p1Ship_x[x]][p1Ship_y[x]] = "S"
        except TypeError:
            if isinstance(p1Ship_y[x], int):
                for m in range(0, len(p1Ship_x[x])):
                    p1Board[p1Ship_x[x][m]][p1Ship_y[x]] = "S"
            else:
                for m in range(0, len(p1Ship_y[x])):
                    p1Board[p1Ship_y[x][m]][p1Ship_x[x]] = "S"
    print_board(p1Board, xLine, yLine)

def shot_miss(board, guessX, guessY):
    print ("You missed my battleship!")
    board[guessX][guessY] = "X"
    sleep(1)

def guess_cal(shots, p1Ship_x, p1Ship_y, p2Board, p1Ships_Sunk, p2Ships_Sunk, p1, p2, pTurn, xLine, yLine):
    while True:
        try:
            sleep(1)
            print (" ")
            print ("Player " + str(p2) + "'s board.")
            print (" ")
            print_board(p2Board, xLine, yLine)
            print (" ")
            print ("Player " + str(p1) + "'s Turn!")
            print (str(shots) + " shots remaning.")
            if (pTurn == 1):
                print (str(p2Ships_Sunk) + " of player " + str(p2) + "'s ships have been sunk by player " + str(p1) + ".")
            else:
                print (str(p1Ships_Sunk) + " of player " + str(p2) + "'s ships have been sunk by player " + str(p1) + ".")
            guessY = int(input("Please enter your number for the x-axis: "))
            guessX = int(input("Please enter your number for the y-axis: "))
        except ValueError:
            print ("Please enter an integer.")
            continue
        else:
            if guessX < 0 or guessX > size-1 or guessY < 0 or guessY > size-1:
                print ("Your shot landed outside of the battlezone. Please try again.")
                sleep(1)
                return p1Ships_Sunk, p2Ships_Sunk
            elif p2Board[guessX][guessY] == "E" or p2Board[guessX][guessY] == "X":
                print ("You have already guessed that. Please try again.")
                sleep(1)
                continue
            elif guessX not in p1Ship_x and guessY not in p1Ship_y:
                shot_miss(p2Board, guessX, guessY)
                return p1Ships_Sunk, p2Ships_Sunk
            try:
                x2 = p1Ship_x.index(guessX)
                y2 = p1Ship_y.index(guessY)
                if (isinstance(p1Ship_y[x2], int) and isinstance(p1Ship_x[x2], int)) and (isinstance(p1Ship_y[y2], int) and isinstance(p1Ship_x[y2], int)):
                    try:
                        if p1Ship_y.index(guessY) == p1Ship_x.index(guessX):
                            x_Index = p1Ship_x.index(guessX)
                            y_Index = p1Ship_y.index(guessY) if guessY in p1Ship_y else -1
                            if guessX == p1Ship_x[x_Index] and guessY == p1Ship_y[y_Index]:
                                print ("You sunk one of my battleships!")
                                p2Board[guessX][guessY] = "E"
                                p1Ship_x.remove(guessX)
                                p1Ship_y.remove(guessY)
                                if pTurn == 2:
                                    p1Ships_Sunk += 1
                                else:
                                    p2Ships_Sunk += 1
                                sleep(1)
                                return p1Ships_Sunk, p2Ships_Sunk
                            print (x_Index)
                        else:
                            shot_miss(p2Board, guessX, guessY)
                            return p1Ships_Sunk, p2Ships_Sunk
                    except ValueError:
                        shot_miss(p2Board, guessX, guessY)
                        return p1Ships_Sunk, p2Ships_Sunk
                else:
                    raise ValueError
            except ValueError:
                try:
                    if isinstance(p1Ship_x.index(guessX), int):
                        try:
                            x2 = p1Ship_x.index(guessX)
                            if guessY == p1Ship_y[x2] or guessY in p1Ship_y[x2]:
                                y_Index = p1Ship_y[x2].index(guessY)
                            else:
                                shot_miss(p2Board, guessX, guessY)
                                return p1Ships_Sunk, p2Ships_Sunk
                            x_Index = p1Ship_x.index(guessX) if guessX in p1Ship_x else -1
                            if guessY == p1Ship_y[x2][y_Index] and guessX == p1Ship_x[x_Index]:
                                p2Board[guessX][guessY] = "E"
                                p1Ship_y[x2].remove(guessY)
                                if len(p1Ship_y[x_Index]) < 1:
                                    print ("You sunk one of my battleships!")
                                    if pTurn == 2:
                                        p1Ships_Sunk += 1
                                    else:
                                        p2Ships_Sunk += 1
                                    p1Ship_y.remove(p1Ship_y[x_Index])
                                    p1Ship_x.remove(guessX)
                                else:
                                    print ("You damaged one of my battleships!")
                                sleep(1)
                                return p1Ships_Sunk, p2Ships_Sunk
                        except (ValueError, TypeError):
                            shot_miss(p2Board, guessX, guessY)
                            return p1Ships_Sunk, p2Ships_Sunk
                except ValueError:
                    if isinstance(p1Ship_y.index(guessY), int):
                        try:
                            y2 = p1Ship_y.index(guessY)
                            if guessX == p1Ship_x[y2] or guessX in p1Ship_x[y2]:
                                x_Index = p1Ship_x[y2].index(guessX)
                            else:
                                shot_miss(p2Board, guessX, guessY)
                                return p1Ships_Sunk, p2Ships_Sunk
                            y_Index = p1Ship_y.index(guessY) if guessY in p1Ship_y else -1
                            if guessX == p1Ship_x[y2][x_Index] and guessY == p1Ship_y[y_Index]:
                                p2Board[guessX][guessY] = "E"
                                p1Ship_x[y2].remove(guessX)
                                if len(p1Ship_x[y_Index]) < 1:
                                    print ("You sunk one of my battleships!")
                                    if pTurn == 2:
                                        p1Ships_Sunk += 1
                                    else:
                                        p2Ships_Sunk += 1
                                    p1Ship_x.remove(p1Ship_x[y_Index])
                                    p1Ship_y.remove(guessY)
                                else:
                                    print ("You damaged one of my battleships!")
                                sleep(1)
                                return p1Ships_Sunk, p2Ships_Sunk
                        except (ValueError, TypeError):
                            shot_miss(p2Board, guessX, guessY)
                            return p1Ships_Sunk, p2Ships_Sunk

def guess(p, p1shots, p2shots, p1Ships_Sunk, p2Ships_Sunk, ship_Num):
    while True:
        print ("Player 1 ships sunk:" + str(p1Ships_Sunk))
        print ("Player 2 ships sunk:" + str(p2Ships_Sunk))
        pTurn = next(p)
        if p1Ships_Sunk == ship_Num:
            print ("Player 1 have sunken all of player 2's battleships! Player 1 wins!")
            sleep(1)
            print ("Game Over.")
            break
        elif p2Ships_Sunk == ship_Num:
            print ("Player 2 have sunken all of player 1's battleships! Player 2 wins!")
            sleep(1)
            print ("Game Over.")
            break
        elif p1shots == 0:
            print ("Player 1 has ran out of shots!\nGame Over!\nPlayer 2 wins!")
            ship_loc(p2Board, p1Ship_x, p1Ship_y)
            break
        elif p2shots == 0:
            print ("Player 2 has ran out of shots!\nGame Over!\nPlayer 1 wins!")
            ship_loc(p1Board, p1Ship_x, p1Ship_y)
            break
        elif pTurn == 1:
            p1Ships_Sunk, p2Ships_Sunk = guess_cal(p1shots, p2Ship_x, p2Ship_y, p2Board, p1Ships_Sunk, p2Ships_Sunk, p1, p2, pTurn, xLine, yLine)
            p1shots -= 1
            continue
        else:
            p1Ships_Sunk, p2Ships_Sunk = guess_cal(p2shots, p1Ship_x, p1Ship_y, p1Board, p1Ships_Sunk, p2Ships_Sunk, p2, p1, pTurn, xLine, yLine)
            p2shots -= 1
            continue

guess(p, p1shots, p2shots, p1Ships_Sunk, p2Ships_Sunk, ship_Num)
