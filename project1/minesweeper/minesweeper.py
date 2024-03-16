import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if len(self.cells) == self.count:
            return self.cells
        return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0:
            return self.cells
        return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.count -= 1
            self.cells.discard(cell)

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.discard(cell)


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def conclude(self):
        flag = False
        new_mines = []
        new_safes = []
        for sentence in self.knowledge:
            if len(sentence.known_mines()) > 0:
                flag = 1
                new_mines.extend(list(sentence.known_mines()))
            if len(sentence.known_safes()) > 0:
                flag = 1
                new_safes.extend(list(sentence.known_safes()))
        # extend the new discovery
        if len(new_mines) > 0:
            for mine in new_mines:
                self.mark_mine(mine)
        if len(new_safes) > 0:
            for safe in new_safes:
                self.mark_safe(safe)
        return flag
    
    def get_sub(self) :
        flag = False
        new_knowledge = []
        for i in range(0, len(self.knowledge)):
            for j in range(0, len(self.knowledge)):
                if self.knowledge[j].cells.issubset(self.knowledge[i].cells):
                    # j is the subset of i
                    tmp = Sentence(self.knowledge[i].cells - self.knowledge[j].cells,
                                   self.knowledge[i].count - self.knowledge[j].count)
                    tag = True
                    for s in self.knowledge:
                        if s == tmp:
                            tag = False
                            break
                    if tag == False:
                        # already have tmp in knowledge
                        continue
                    new_knowledge.append(tmp)
                    flag = True
        self.knowledge.extend(new_knowledge)
        return flag


    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        self.moves_made.add(cell)
        self.mark_safe(cell)

        x, y = cell
        neighbor = set()
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if 0 <= x + i < self.height and 0 <= y + j < self.width:
                    if (x + i, y + j) in self.mines:
                        count -= 1 # ignore the cells that already were detected as mines
                        continue
                    if (x + i, y + j) in self.safes:
                        continue # we also ignore
                    neighbor.add((x + i, y + j))
        self.knowledge.append(Sentence(neighbor, count))
        
        while True:
            res1 = self.conclude()
            res2 = self.get_sub()
            if res1 == 0 and res2 == 0:
                # no new discovery
                break
        

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        safe_moves = self.safes - self.moves_made
        if len(safe_moves) > 0:
            return list(safe_moves)[0]
        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        random_move = set()
        for i in range(0,self.height):
            for j in range(0,self.width):
                random_move.add((i, j))
        random_move -= self.moves_made
        random_move -= self.mines
        if len(random_move) > 0:
            return list(random_move)[0]
        return None

'''
Reflections:
The most important thing of this AI : We define a new expression of sentence
(cells, count) representing a cell set and how many mines are in it.

if count == 0 : we can conclude all cells are safe .
if count == cells : we can conclude all sells are mines .

otherwise we can process new sentence by doing some subset method
{A1, A2, A3, A4, A5} = C1
{A1, A2, A3} = C2
we can conclude that {A4, A5} = C1 - C2

once we know some cell is mine or safe, remove it from our knowledge base
Keep loop it until we win the game .
'''