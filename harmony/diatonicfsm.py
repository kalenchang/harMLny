from enum import Enum

# class ChordRN(Enum):
#     # Chord Roman Numerals
#     I = 'I'
#     ii = 'ii'
#     iii = 'iii'
#     IV = 'IV'
#     V = 'V'
#     vi = 'vi'
#     viio = 'viio'

# class ChordK(key):

#     def __init__(self, key):
#         for chordsymbol in ChordRN

'''
classicalrules = {
    ChordRN.I: [ChordRN.I, ChordRN.ii, ChordRN.iii, ChordRN.IV, ChordRN.V, ChordRN.vi, ChordRN.viio],
    ChordRN.ii: [ChordRN.ii, ChordRN.IV, ChordRN.V, ChordRN.viio],
    ChordRN.iii: [ChordRN.iii, ChordRN.IV, ChordRN.vi],
    ChordRN.IV: [ChordRN.I, ChordRN.ii, ChordRN.IV, ChordRN.V],
    ChordRN.V: [ChordRN.I, ChordRN.V, ChordRN.vi, ChordRN.viio],
    ChordRN.vi: [ChordRN.ii, ChordRN.IV, ChordRN.vi],
    ChordRN.viio: [ChordRN.I, ChordRN.V, ChordRN.viio]
}
'''

classicalrules = {
    'I': ['I', 'iii', 'S', 'D', 'vi'],
    'iii': ['iii', 'S', 'vi'],
    'S': ['I', 'S', 'D'],
    'D': ['I', 'D', 'vi'],
    'vi': ['S', 'vi']
}

'''
chordsCMajortoRN = {
    'C': ChordRN.I,
    'D': ChordRN.ii,
    'E': ChordRN.iii,
    'F': ChordRN.IV,
    'G': ChordRN.V,
    'A': ChordRN.vi,
    'B': ChordRN.viio
}
'''

def check(pathRN, chorddict=classicalrules):
    # check if a path of chords (ex. path = ['C', 'D', 'G', 'C']) follows the rules of the FSM
    # pathRN = [chordsCMajortoRN[c] for c in path]
    # examplePathRN = [ChordRN.I, ChordRN.vi, ChordRN.IV, ChordRN.V, ChordRN.I]
    if pathRN[0] != 'I':
        return False
    for i in range(len(pathRN) - 1):
        if pathRN[i + 1] not in chorddict[pathRN[i]]:
            return False
    return True