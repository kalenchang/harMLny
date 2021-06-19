# random not viterbi
# constructs all valid chord-chord transitions, then removes all dead ends
# then selects transitions at random until a chord progression for the melody is constructed
import random

chords = ["I", "ii", "iii", "IV", "V", "vi", "viio"]
start_p = {"I": 1, "ii": 0, "iii": 0, "IV": 0, "V": 0, "vi": 0, "viio": 0}

chordPossDict = {
    1 : ['I', 'IV', 'vi'],
    2 : ['ii', 'V', 'viio'],
    3 : ['I', 'iii', 'vi'],
    4 : ['ii', 'IV', 'viio'],
    5 : ['I', 'iii', 'V'],
    6 : ['ii', 'IV', 'vi'],
    7 : ['iii', 'V', 'viio']
}

trans_p = {
    "I": {"I": 0.23, "ii": 0.11, "iii": 0, "IV": 0.22, "V": 0.31, "vi": 0.08, "viio": 0.02},
    "ii": {"I": 0, "ii": 0.14, "iii": 0, "IV": 0, "V": 0.45, "vi": 0, "viio": 0.23},
    "iii": {"I": 0, "ii": 0.2, "iii": 0.05, "IV": 0.25, "V": 0, "vi": 0.4, "viio": 0},
    "IV": {"I": 0.24, "ii": 0.12, "iii": 0, "IV": 0.1, "V": 0.29, "vi": 0, "viio": 0.18},
    "V": {"I": 0.67, "ii": 0, "iii": 0, "IV": 0, "V": 0.15, "vi": 0.11, "viio": 0},
    "vi": {"I": 0.11, "ii": 0.22, "iii": 0, "IV": 0.18, "V": 0.21, "vi": 0.1, "viio": 0.11},
    "viio": {"I": 0.81, "ii": 0, "iii": 0, "IV": 0, "V": 0.06, "vi": 0, "viio": 0}
}

new_trans_p = {
    "I": {"I": 0.23, "ii": 0.11, "iii": 0, "IV": 0.22, "V": 0.31, "vi": 0.08, "viio": 0.02},
    "ii": {"I": 0, "ii": 0.14, "iii": 0, "IV": 0, "V": 0.45, "vi": 0, "viio": 0.23},
    "iii": {"I": 0, "ii": 0.2, "iii": 0.05, "IV": 0.25, "V": 0, "vi": 0.4, "viio": 0},
    "IV": {"I": 0.24, "ii": 0.12, "iii": 0, "IV": 0.1, "V": 0.29, "vi": 0, "viio": 0.18},
    "V": {"I": 0.67, "ii": 0, "iii": 0, "IV": 0, "V": 0.15, "vi": 0.11, "viio": 0},
    "vi": {"I": 0.11, "ii": 0.22, "iii": 0, "IV": 0.18, "V": 0.21, "vi": 0.1, "viio": 0.11},
    "viio": {"I": 0.81, "ii": 0, "iii": 0, "IV": 0, "V": 0.06, "vi": 0, "viio": 0},
}


def createtree(melody, chords, equalProb=False):

    chordlist = [] # a list of lists x, where x_i is all the chords that can go with melody note i. start/end on tonic
    # melodyNums = []
    for i in range(0, len(melody)):
        # melodyNums.append(localMelodyNum)
        if (i == 0) or (i == len(melody) - 1):
            chordlist.append(['I'])
        else:
            chordlist.append(chordPossDict[melody[i]])
        

    # create list of possible chord transitions
    transitions = []
    for i in range(len(chordlist) - 1):
        transitions.append([])
        for c1 in chordlist[i]:
            for c2 in chordlist[i+1]:
                if trans_p[c1][c2] > 0:
                    transitions[i].append((c1,c2,trans_p[c1][c2]))
    # print('before')
    # print(transitions)

    def validtrans(t, i, nexts):
        if i == 0:
            return t[1] == 'I'
        else:
            return t[1] in nexts

    # prune dead ends
    for i in range(len(transitions)): # 0 1 2 ...  n-1
        nexts = [tx[0] for tx in transitions[-i]]
        transitions[-1-i] = [t for t in transitions[-1-i] if validtrans(t, i, nexts)]
    # print('after')
    # print(transitions)

    def nextchord(transitions):
        total_probability = sum([p for (c1, c2, p) in transitions])
        random_number = random.uniform(0, total_probability)
        for (c1, c2, p) in transitions:
            random_number -= p
            if random_number <= 0:
                return c2

    # construct a complete path by choosing transitions at random
    path = [chordlist[0][0]]
    for i in range(len(transitions)):
        # print('path: ' + str(path))
        # print('trans: ' + str(transitions[i]))
        if equalProb:
            # this one will choose a random next chord with equal probability for each
            chordchoices = [t[1] for t in transitions[i] if t[0] == path[i]]
            path.append(chordchoices[random.randint(0,len(chordchoices)-1)])
        else:
            # this one will choose a random next chord based on the probabilities from the table
            path.append(nextchord(transitions[i]))
    
    return(path)

if __name__ == "__main__":

    # mel = [1,2,3,4,5,1]
    mel = [1,2,3,4,5,3,4,2,1,2,3,4,2,3,7,1]
    # seems to handle long melodies w/ no problem

    print('melody:' + str(mel))

    chordProg = createtree(mel, chords)
    print(chordProg)
