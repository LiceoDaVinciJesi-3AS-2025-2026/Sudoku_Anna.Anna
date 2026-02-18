from sudoku9 import SudokuGenerator

generator = SudokuGenerator(difficulty="hard")
puzzle = generator.get_puzzle()

for row in puzzle:
    print(" ".join(row))

griglia = [
    "53..7....",
    "6..195...",
    ".98....6.",
    "8...6...3",
    "4..8.3..1",
    "7...2...6",
    ".6....28.",
    "...419..5",
    "....8..79"]


lista_numeri = [1, 2, 3, 4, 5, 6, 7, 8, 9]
lista = []

# generare ogni volta un sudoku diverso
# 







