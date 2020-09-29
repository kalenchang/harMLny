from music21 import *


def isNotForbiddenParallel(prevInt, currInt):
    if prevInt.name != currInt.name:
        return True
    else:
        return currInt.name not in ('P4', 'P5', 'P8')


def isValidMelodicInterval(iv):  #interval
    return iv.name in ('P4', 'P5', 'P8', 'm2', 'M2', 'm3', 'M3') or iv.semitones == 8
    # needs to count semitones for ASCENDING m6 only


def isNotHiddenParallel(cfInt, cpInt, harmInt):
    # check if cfInt and cpInt are in the same direction (similar motion)
    if harmInt.name in ('P4', 'P5', 'P8') and cfInt.semitones * cpInt.semitones > 0:
        return cfInt.isStep or cpInt.isStep
    else:
        return True


def isNotSimilarSkip(cfInt, cpInt):
    return cfInt.isStep or cpInt.isStep or cfInt.semitones * cpInt.semitones <= 0


def isInKey(scale, note):
    return (note.name in scale)


def contraryMotionScore(cfNotes, path):
    assert len(cfNotes) == len(path) # for first species, cf and cp need to have the same number of notes
    rawScore = 0
    # for each two consecutive intervals that are not equal, add 1 to raw score
    for i in range(len(cfNotes) - 1):
        cpInterval = interval.Interval(path[i], path[i + 1])
        cfInterval = interval.Interval(cfNotes[i], cfNotes[i + 1])
        if (cpInterval.semitones * cfInterval.semitones < 0):
            rawScore += 1
    normalizedScore = rawScore / (len(cfNotes) - 1)
    return normalizedScore


def perfectIntervalScore(cfNotes, path):
    "Returns score of (num of imperfect intervals) / (num of notes - 2)"
    assert len(cfNotes) == len(path) # for first species, cf and cp need to have the same number of notes
    rawScore = 0
    # for each two consecutive intervals that are not equal, add 1 to raw score
    for i in range(len(cfNotes)):
        currInterval = interval.Interval(cfNotes[i], path[i])
        if currInterval.name not in ('P1', 'P4', 'P5', 'P8'):
            rawScore += 1
    normalizedScore = rawScore / (len(cfNotes) - 2)
    return normalizedScore


def followSkipScore(path):
    "Returns score of (num skips followed by op dir + 0.5 num skips followed by same dir step) / (number of skips)"
    previousSkip = 0
    numSkipsFollowedOp = 0 # number of skips followed by opposite direction
    numSkipsFollowedSame = 0 # number of skips followed by same direction skip
    numSkips = 0 # number of skips
    for i in range(len(path) - 1):
        semitones = interval.Interval(path[i], path[i + 1]).semitones
        if previousSkip != 0:
            if previousSkip * semitones < 0:
                numSkipsFollowedOp += 1
            elif semitones == 1 or semitones == 2:
                numSkipsFollowedSame += 0.5
        if semitones > 4:
            numSkips += 1
            previousSkip = semitones
        else:
            previousSkip = 0
    return 1.0 if numSkips == 0 else (numSkipsFollowedOp + numSkipsFollowedSame) / numSkips        


def determineFirstSpecies(cfLine, cfScale):
    cp = stream.Part()
    piano = instrument.Piano()
    cp.insert(0, piano)
    cp.priority = -1

    cpNotePoss = []
    cpArrowPoss = []

    for cfMeasure in cfLine.getElementsByClass(stream.Measure):
        cfMeasureNumber = cfMeasure.number
        # print(cfMeasureNumber)

        cpNotePoss.append([])
        cpArrowPoss.append([])

        cfNote = cfMeasure.getElementsByClass(note.Note)[0] # aka cfCurrent
        if cfMeasureNumber > 1:
            # TODO: clean this line up
            cfPrevious = cfLine.getElementsByClass(stream.Measure)[cfMeasureNumber-2].getElementsByClass(note.Note)[0]

        if cfMeasureNumber == 1:
            cpNotePoss[cfMeasureNumber - 1].append(cfNote.transpose('p1'))
            cpNotePoss[cfMeasureNumber - 1].append(cfNote.transpose('p5'))
            cpNotePoss[cfMeasureNumber - 1].append(cfNote.transpose('p8'))
        elif cfMeasureNumber == len(cfLine.getElementsByClass(stream.Measure)):
            cpNotePoss[cfMeasureNumber - 1].append(cfNote.transpose('p1'))
            cpNotePoss[cfMeasureNumber - 1].append(cfNote.transpose('p8'))

            # only allow melodic steps
            for cpCurrent in cpNotePoss[cfMeasureNumber - 1]:
                harmIntCurrent = interval.Interval(cfNote, cpCurrent)
                for cpPrevious in cpNotePoss[cfMeasureNumber - 2]:
                    harmIntPrevious = interval.Interval(cfPrevious, cpPrevious)
                    if interval.Interval(cpPrevious, cpCurrent).isStep \
                            and isNotForbiddenParallel(harmIntPrevious, harmIntCurrent):
                        cpArrowPoss[cfMeasureNumber - 2].append((cpPrevious, cpCurrent))
        else:
            melIntNotes = [cfNote.transpose('m3'), 
                cfNote.transpose('M3'), 
                cfNote.transpose('P4'), 
                cfNote.transpose('P5'), 
                cfNote.transpose('m6'), 
                cfNote.transpose('M6'), 
                cfNote.transpose('P8'), 
                cfNote.transpose('m10'), 
                cfNote.transpose('M10')
            ]
            for melintnote in melIntNotes:
                if isInKey(cfScale, melintnote):
                    cpNotePoss[cfMeasureNumber - 1].append(melintnote)

            # only allow certain melodic intervals
            for cpCurrent in cpNotePoss[cfMeasureNumber - 1]:
                harmIntCurrent = interval.Interval(cfNote, cpCurrent)
                for cpPrevious in cpNotePoss[cfMeasureNumber - 2]:
                    harmIntPrevious = interval.Interval(cfPrevious, cpPrevious)
                    cfMelodicInterval = interval.Interval(cfPrevious, cfNote)
                    cpMelodicInterval = interval.Interval(cpPrevious, cpCurrent)

                    if isValidMelodicInterval(cpMelodicInterval) \
                            and isNotForbiddenParallel(harmIntPrevious, harmIntCurrent) \
                            and isNotHiddenParallel(cfMelodicInterval, cpMelodicInterval, harmIntCurrent) \
                            and isNotSimilarSkip(cfMelodicInterval, cpMelodicInterval):
                        cpArrowPoss[cfMeasureNumber - 2].append((cpPrevious, cpCurrent))

    # find all paths
    # pathsFound is a list of dictionaries. first list corresponds to the measures, the dictionary corresponds to the notes in cpNotePoss
    pathsFound = []
    for measurenumber in range(len(cpNotePoss)):
        pathsFound.append({})
        for noten in cpNotePoss[measurenumber]:
            paths = []
            if measurenumber == 0:
                paths = [[noten]]
            else:
                for arrow in cpArrowPoss[measurenumber-1]:
                    if noten == arrow[1]:
                        for path in pathsFound[measurenumber-1][(arrow[0].name + str(arrow[0].octave))]:
                            paths.append(path+[noten])
            pathsFound[measurenumber][(noten.name + str(noten.octave))] = paths
    
    cfNotes = cfLine.flat.getElementsByClass(note.Note)
    print('[' + ', '.join([(notem.name + str(notem.octave)) for notem in cfNotes]) + ']')

    pathsToBeScored = []
    highestScore = 0
    highestScoringPaths = []
    for pathlist in pathsFound[len(cpNotePoss) - 1].values():
        for path in pathlist:
            if validTwoSkips(path) and noDissonantOutline(path) and hasValidClimax(path) and noFourParallels(cfNotes, path):
                pathsToBeScored.append(path)
                # calc score vector [contrary motion, follow skip opp dir, climax near middle]
                weights = [0.8, 0.9, 0.6, 0.7]
                scores = [contraryMotionScore(cfNotes, path), followSkipScore(path), round(climaxScore(path), 2), round(perfectIntervalScore(cfNotes, path), 2)]
                embedding = [weights[i] * scores[i] for i in range(len(scores))]
                finalScore = round(sum(embedding), 2)
                print('[' + ', '.join([(notem.name + str(notem.octave)) for notem in path]) + '], scores: ' + str(scores) + ', final score: ' + str(finalScore))

                if finalScore > highestScore:
                    highestScore = finalScore
                    highestScoringPaths = [path]
                elif finalScore == highestScore:
                    highestScoringPaths.append(path)
                
            # elif not noFourParallels(cfNotes, path):
                # print('fOUR PARALLESL: [' + ', '.join([(notem.name + str(notem.octave)) for notem in path]) + ']')
    
    for path in highestScoringPaths:
        print('[' + ', '.join([(notem.name + str(notem.octave)) for notem in path]) + ']')
    print('final score: ' + str(highestScore))
    print('[' + ', '.join([(notem.name + str(notem.octave)) for notem in cfNotes]) + ']')
            


def validTwoSkips(path):
    for i in range(len(path)-2):
        thisInt = interval.Interval(path[i], path[i+1])
        if abs(thisInt.semitones) > 4:
            nextInt = interval.Interval(path[i+1], path[i+2])
            if abs(nextInt.semitones) > 4 and thisInt.semitones * nextInt.semitones > 0:
                # this is the code for 2 skips in SAME direction
                # check if second skip is smaller than first
                if abs(nextInt.semitones) > abs(thisInt.semitones):
                    return False
                # check if combined interval is consonant
                if interval.Interval(path[i], path[i+2]).name not in ('m6', 'M6', 'P8', 'm9', 'M9', 'm10', 'M10'):
                    return False
    return True


def noDissonantOutline(path):
    localminmax = 0
    localint = interval.Interval(path[0], path[1])
    direction = 0 if localint.semitones == 0 else localint.semitones / abs(localint.semitones)
    for i in range(1, len(path) - 1):
        localint = interval.Interval(path[i], path[i + 1])
        newdirection = 0 if localint.semitones == 0 else localint.semitones / abs(localint.semitones)
        if direction != newdirection:
            overarchingint = interval.Interval(path[localminmax], path[i])
            if overarchingint.semitones in (6, 10, 11):
                return False
            localminmax = i
            direction = newdirection
    return True


def findClimax(path):
    climax = path[0]
    for n in path[1:]:
        testint = interval.Interval(climax, n)
        if testint.semitones > 0:
            climax = n
    return climax # returns note


def findClimaxIndex(path):
    climax = 0
    for i in range(1, len(path)):
        testint = interval.Interval(path[climax], path[i])
        if testint.semitones > 0:
            climax = i
    return climax # returns index of climax


def hasValidClimax(path):
    climax = findClimax(path)
    climaxCount = 0
    for n in path:
        if n == climax:
            climaxCount += 1
    return path[0] != climax and path[-1] != climax and climaxCount == 1


#TODO: doesn't work, but not necessary (use non-alt function)
def hasValidClimaxAlt(path):
    climax = path[0]
    climaxCount = 1
    for n in path[1:]:
        testint = interval.Interval(climax, n)
        if testint.semitones > 0:
            climax = n
            climaxCount = 1
        elif testint.semitones == 0:
            climaxCount += 1
    return True


def climaxScore(path):
    '''This function returns a score of how close the climax is to the center
        of the path, according to the following formula (latex):
        $$y = \left(1-\left(\frac{x-3.5}{3.5}\right)^2\right)^{0.8}$$'''
    climaxIndex = findClimaxIndex(path)
    graphshift = (len(path) - 1) / 2
    return (1 - (((climaxIndex - graphshift) / graphshift) ** 2)) ** 0.8


def noFourParallels(cfNotes, path):
    numParallels = 0
    for i in range(len(path)-1):
        currInt = interval.Interval(cfNotes[i], path[i])
        nextInt = interval.Interval(cfNotes[i+1], path[i+1])
        if currInt.semitones == nextInt.semitones:
            numParallels += 1
            if numParallels > 3:
                return False
        else:
            numParallels = 0
    return True

    '''
        print(cfNote.name + ': ', end='')
        for cpNP in cpNotePoss[cfMeasureNumber - 1]:
            print(cpNP.name + ', ', end='')
        print('===', end=' ')
        if cfMeasureNumber >= 2:
            for cpAP in cpArrowPoss[cfMeasureNumber - 2]:
                print(cpAP[0].name + '->' + cpAP[1].name, end=' ')
        print()

    
    noteList = []

    for cfmeasure in cf.getElementsByClass('Measure'):
        cpmeasure = stream.Measure()


        cpmeasure.append(note.Note(noteList[i], quarterLength=4))


        cp.append(cpmeasure)
    return cp
    '''


if __name__ == "__main__":

    cmajorscale = ['C', 'D', 'E', 'F', 'G', 'A', 'B']

    source = converter.parse('cpt/cf4.mxl')
    # source.show('text')

    # cantus firmus
    cf = source.parts[0]
    # print(cf)

    # contra punctum
    cp = determineFirstSpecies(cf, cmajorscale)

    '''

    # get time signature from cf and add time signature to cp
    cp.measure(1).insert(0, cf.flat.getElementsByClass(meter.TimeSignature)[0])

    source.insert(0, cp)
    '''
    # source.show('text')
    # source.show()
