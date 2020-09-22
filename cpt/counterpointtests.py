from counterpoint import *

# contraryMotionScore unit tests
testCF1 = converter.parse('cf3.mxl').parts[0]
testPath1 = [note.Note('C4'), note.Note('C4'), note.Note('C4'), note.Note('C4'), note.Note('C4'), note.Note('G4')]
assert contraryMotionScore(testCF1, testPath1) == 0.2

testCF2 = converter.parse('cf3.mxl').parts[0]
testPath2 = [note.Note('C4'), note.Note('A3'), note.Note('G3'), note.Note('A3'), note.Note('B3'), note.Note('C4')]
assert contraryMotionScore(testCF2, testPath2) == 1

print("CONGRATS!")