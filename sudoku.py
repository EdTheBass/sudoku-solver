import random as rand
import time

class Grid:
    def __init__(self, cells=[]):
        self.cells = cells
        self.wave = []

        if not cells:
            self.reset()
        
        self.propagate()

    def reset(self):
        self.cells = [[0]*9,[0]*9,[0]*9,[0]*9,[0]*9,[0]*9,[0]*9,[0]*9,[0]*9]
        self.propagate()

    def get(self, coord):
        r,c = coord
        return self.cells[r][c]

    def set(self, coord, num):
        r,c = coord
        self.cells[r][c] = num
        self.propagate()

    def get_columns(self):
        cols = [[],[],[],[],[],[],[],[],[]]
        for row in self.cells:
            for k in range(9):
                cols[k].append(row[k])
        return cols
    
    def get_blocks(self):
        bks = [[],[],[],[],[],[],[],[],[]]
        for r,row in enumerate(self.cells):
            for k in range(9):
                bks[3*(r//3)+k//3].append(row[k])
        return bks
    
    def is_solved(self):
        columns = self.get_columns()
        # blocks defined left to right, top to bottom, same with internal block structure
        blocks = self.get_blocks()
        for row in self.cells:
            if 0 in row:
                return False
            if len(list(set(row))) != 9:
                return False

        for i in range(9):
            if len(list(set(columns[i]))) != 9 or len(list(set(blocks[i]))) != 9:
                return False
        
        return True
    
    def is_filled(self):
        for row in self.cells:
            if 0 in row:
                return False
        return True

    def show(self):
        print("|===========|")
        for i,row in enumerate(self.cells):
            print("|",end="")
            for j,cell in enumerate(row):
                f_cell = cell if cell else " "
                print(f_cell, end="")
                if (j+1)%3 == 0 and j != 8: print("|", end="")
            print("|")
            if (i+1)%3 == 0: print("|===========|")
        print()

    def solve(self):
        moves = []
        while not self.is_filled():
            next_move = self.next_move()
            if next_move == [-1,-1]:
                # backtrack
                last_move = moves.pop()
            else:
                moves.append(next_move)

    def next_move(self):
        minimum = 1e100
        coord = [-1,-1]
        for i in range(9):
            for j in range(9):
                n_choices = len(self.wave[i][j])
                if n_choices < minimum and n_choices:
                    minimum = n_choices
                    coord = [i,j]

        if minimum == 1e100:
            return coord

        r,c = coord
        choices = self.wave[r][c]
        self.set(coord, rand.choice(choices))
        return coord

    def propagate(self,coord=[]):
        self.wave = [[[] for _ in range(9)] for __ in range(9)]

        columns = self.get_columns()
        blocks = self.get_blocks()

        if not coord:
            for i in range(9):
                for j in range(9):
                    if self.get([i,j]):
                        continue

                    curr_row = self.cells[i]
                    curr_col = columns[j]
                    curr_block = blocks[3*(i//3)+j//3]
                    rcb = curr_row + curr_col + curr_block

                    self.wave[i][j] = [n for n in range(1,10) if n not in rcb]
            return
        
        r,c = coord
        num = self.get([r,c])
        curr_row = self.cells[r]
        curr_col = columns[c]
        curr_block = blocks[3*(r//3)+c//3]
        for i in range(9):
            try: self.wave[i][c].remove(num)
            except ValueError: pass
            try: self.wave[r][i].remove(num)
            except ValueError: pass
        xmin,xmax = -(r%3)
        ymin,ymax = -(c%3)
        for i in range(xmin,xmax+1):
            for j in range(ymin,ymax+1):
                try: self.wave[i][j].remove(num)
                except ValueError: continue
                       
                
solved = [[5,3,4,6,7,8,9,1,2],
             [6,7,2,1,9,5,3,4,8],
             [1,9,8,3,4,2,5,6,7],
             [8,5,9,7,6,1,4,2,3],
             [4,2,6,8,5,3,7,9,1],
             [7,1,3,9,2,4,8,5,6],
             [9,6,1,5,3,7,2,8,4],
             [2,8,7,4,1,9,6,3,5],
             [3,4,5,2,8,6,1,7,9]]
test = [[5,3,0,0,7,0,0,0,0],
        [6,0,0,1,9,5,0,0,0],
        [0,9,8,0,0,0,0,6,0],
        [8,0,0,0,6,0,0,0,3],
        [4,0,0,8,0,3,0,0,1],
        [7,0,0,0,2,0,0,0,6],
        [0,6,0,0,0,0,2,8,0],
        [0,0,0,4,1,9,0,0,5],
        [0,0,0,0,8,0,0,7,9]]
test2 = [[0,8,0,0,0,6,2,0,0],
         [5,0,0,8,7,0,3,0,0],
         [0,0,0,0,0,4,0,7,0],
         [0,4,0,2,1,0,0,3,0],
         [0,0,9,0,0,0,5,0,0],
         [0,0,0,0,0,7,0,0,0],
         [0,0,0,6,0,0,0,0,0],
         [0,2,0,3,8,0,0,1,0],
         [4,0,0,0,0,0,0,0,2]]

grid = Grid(test2)
grid.show()
start = time.time()
grid.solve()
print(f"{time.time()-start:0.5f}")
grid.show()
