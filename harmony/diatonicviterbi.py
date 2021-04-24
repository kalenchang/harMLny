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
    "I": {"I": 0.23, "ii": 0.11, "iii": 0.01, "IV": 0.22, "V": 0.31, "vi": 0.08, "viio": 0.02},
    "ii": {"I": 0.08, "ii": 0.14, "iii": 0.01, "IV": 0.02, "V": 0.45, "vi": 0.06, "viio": 0.23},
    "iii": {"I": 0, "ii": 0.2, "iii": 0.05, "IV": 0.25, "V": 0.05, "vi": 0.4, "viio": 0.05},
    "IV": {"I": 0.24, "ii": 0.12, "iii": 0.02, "IV": 0.1, "V": 0.29, "vi": 0.04, "viio": 0.18},
    "V": {"I": 0.67, "ii": 0.01, "iii": 0.01, "IV": 0.04, "V": 0.15, "vi": 0.11, "viio": 0},
    "vi": {"I": 0.11, "ii": 0.22, "iii": 0.06, "IV": 0.18, "V": 0.21, "vi": 0.1, "viio": 0.11},
    "viio": {"I": 0.81, "ii": 0, "iii": 0.04, "IV": 0.06, "V": 0.06, "vi": 0.04, "viio": 0},
}

def viterbi(melody, chords, start_p, trans_p):
    V = [{}]
    for ch in chords:
        V[0][ch] = {"prob": start_p[ch], "prev": None}
    # Run Viterbi when t > 0
    for t in range(1, len(melody)):
        V.append({})
        for ch in chords:
            if ch in chordPossDict[melody[t]]:
                melody_multiplier = 1
            else:
                melody_multiplier = 0.1
            max_tr_prob = V[t - 1][chords[0]]["prob"] * trans_p[chords[0]][ch] * melody_multiplier
            prev_st_selected = chords[0]
            for prev_st in chords[1:]:
                tr_prob = V[t - 1][prev_st]["prob"] * trans_p[prev_st][ch] * melody_multiplier
                if tr_prob > max_tr_prob:
                    max_tr_prob = tr_prob
                    prev_st_selected = prev_st

            max_prob = max_tr_prob
            V[t][ch] = {"prob": max_prob, "prev": prev_st_selected}

    # for line in dptable(V):
    #     print(line)

    opt = []
    max_prob = 0.0
    best_st = None
    # Get most probable state and its backtrack
    for ch, data in V[-1].items():
        if data["prob"] > max_prob:
            max_prob = data["prob"]
            best_st = ch
    opt.append(best_st)
    previous = best_st

    # Follow the backtrack till the first observation
    for t in range(len(V) - 2, -1, -1):
        opt.insert(0, V[t + 1][previous]["prev"])
        previous = V[t + 1][previous]["prev"]

    print ("The steps of chords are " + " ".join(opt) + " with highest probability of %s" % max_prob)


if __name__ == "__main__":

    mel = [1,2,3,5,6,1]
    
    print('melody:' + str(mel))

    chordProg = viterbi(mel, chords, start_p, trans_p)
