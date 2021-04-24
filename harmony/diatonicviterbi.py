chords = ("I", "ii", "iii", "IV", "V", "vi", "viio")
start_p = {"I": 0.8, "V": 0.2}
# TODO: get actual probabilities somewhere (these are dummy)
trans_p = {
    "I": {"I": 0.1, "ii": 0.2, "iii": 0.1, "IV": 0.2, "V": 0.1, "vi": 0.2, "viio": 0.1},
    "ii": {"I": 0.1, "ii": 0.2, "iii": 0.1, "IV": 0.2, "V": 0.1, "vi": 0.2, "viio": 0.1},
    "iii": {"I": 0.1, "ii": 0.2, "iii": 0.1, "IV": 0.2, "V": 0.1, "vi": 0.2, "viio": 0.1},
    "IV": {"I": 0.1, "ii": 0.2, "iii": 0.1, "IV": 0.2, "V": 0.1, "vi": 0.2, "viio": 0.1},
    "V": {"I": 0.1, "ii": 0.2, "iii": 0.1, "IV": 0.2, "V": 0.1, "vi": 0.2, "viio": 0.1},
    "vi": {"I": 0.1, "ii": 0.2, "iii": 0.1, "IV": 0.2, "V": 0.1, "vi": 0.2, "viio": 0.1},
    "viio": {"I": 0.1, "ii": 0.2, "iii": 0.1, "IV": 0.2, "V": 0.1, "vi": 0.2, "viio": 0.1},
}

def viterbi(melody, chords, start_p, trans_p):
    V = [{}]
    for ch in chords:
        V[0][ch] = {"prob": start_p[ch], "prev": None}
    # Run Viterbi when t > 0
    for t in range(1, len(melody)):
        V.append({})
        for ch in chords:
            max_tr_prob = V[t - 1][chords[0]]["prob"] * trans_p[chords[0]][ch]
            prev_st_selected = chords[0]
            for prev_st in chords[1:]:
                tr_prob = V[t - 1][prev_st]["prob"] * trans_p[prev_st][ch]
                if tr_prob > max_tr_prob:
                    max_tr_prob = tr_prob
                    prev_st_selected = prev_st

            max_prob = max_tr_prob[melody[t]]
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