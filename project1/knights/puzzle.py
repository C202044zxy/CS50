from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    AKnave
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
puzzle1_Asays = And(AKnave, BKnave)
knowledge1 = And(
    Implication(AKnave, Not(puzzle1_Asays)),
    Implication(AKnight, puzzle1_Asays),
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave))

)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
puzzle2_Asays = Or(And(AKnight, BKnight), And(AKnave, BKnave))
puzzle2_Bsays = Or(And(AKnight, BKnave), And(AKnave, BKnight))

knowledge2 = And(
    Implication(AKnave, Not(puzzle2_Asays)),
    Implication(AKnight, puzzle2_Asays),
    Implication(BKnave, Not(puzzle2_Bsays)),
    Implication(BKnight, puzzle2_Bsays),
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave))

)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
x = Symbol("A : I am a knight")
y = Symbol("B : I am a knave")
puzzle3_Asays = Or(x, y)
puzzle3_Bsays1 = y
puzzle3_Bsays2 = CKnave
puzzle3_Csays = AKnight
knowledge3 = And(
    Implication(x, AKnight),
    Implication(AKnight, puzzle3_Asays),
    Implication(AKnave, Not(puzzle3_Asays)),
    Implication(BKnight, puzzle3_Bsays1),
    Implication(BKnave, Not(puzzle3_Bsays1)),
    Implication(BKnight, puzzle3_Bsays2),
    Implication(BKnave, Not(puzzle3_Bsays2)),
    Implication(CKnight, puzzle3_Csays),
    Implication(CKnave, Not(puzzle3_Csays)),
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),
    Or(CKnight, CKnave),
    Not(And(CKnight, CKnave))

    # TODO
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
