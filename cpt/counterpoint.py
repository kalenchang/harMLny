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
    if harmInt.name in ('P5', 'P8') and cfInt.semitones * cpInt.semitones > 0:
        return cfInt.isStep or cpInt.isStep
    else:
        return True


def isNotSimilarSkip(cfInt, cpInt):
    return cfInt.isStep or cpInt.isStep or cfInt.semitones * cpInt.semitones <= 0


def isInKey(scale, note):
    return (note.name in scale)


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
                harmIntCurrent = interval.Interval(noteStart=cfNote, noteEnd=cpCurrent)
                for cpPrevious in cpNotePoss[cfMeasureNumber - 2]:
                    harmIntPrevious = interval.Interval(noteStart=cfPrevious, noteEnd=cpPrevious)
                    if interval.Interval(noteStart=cpPrevious, noteEnd=cpCurrent).isStep \
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
                harmIntCurrent = interval.Interval(noteStart=cfNote, noteEnd=cpCurrent)
                for cpPrevious in cpNotePoss[cfMeasureNumber - 2]:
                    harmIntPrevious = interval.Interval(noteStart=cfPrevious, noteEnd=cpPrevious)
                    cfMelodicInterval = interval.Interval(noteStart=cfPrevious, noteEnd=cfNote)
                    cpMelodicInterval = interval.Interval(noteStart=cpPrevious, noteEnd=cpCurrent)

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
    
    for pathlist in pathsFound[len(cpNotePoss) - 1].values():
        for path in pathlist:
            print('[' + ', '.join([notem.name for notem in path]) + ']')

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

cmajorscale = ['C', 'D', 'E', 'F', 'G', 'A', 'B']

source = converter.parse('cpt/cf3.mxl')
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
