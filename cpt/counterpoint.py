from music21 import *


def isNotForbiddenParallel(prevInt, currInt):
    if prevInt.name != currInt.name:
        return True
    else:
        return currInt.name not in ('P4', 'P5', 'P8')

def isValidMelodicInterval(iv): #interval
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

def determineFirstSpecies(cfLine):
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
            cpNotePoss[cfMeasureNumber - 1].append(cfNote.transpose('m3'))
            cpNotePoss[cfMeasureNumber - 1].append(cfNote.transpose('M3'))
            cpNotePoss[cfMeasureNumber - 1].append(cfNote.transpose('p4'))
            cpNotePoss[cfMeasureNumber - 1].append(cfNote.transpose('p5'))
            cpNotePoss[cfMeasureNumber - 1].append(cfNote.transpose('m6'))
            cpNotePoss[cfMeasureNumber - 1].append(cfNote.transpose('M6'))
            cpNotePoss[cfMeasureNumber - 1].append(cfNote.transpose('p8'))
            cpNotePoss[cfMeasureNumber - 1].append(cfNote.transpose('m10'))
            cpNotePoss[cfMeasureNumber - 1].append(cfNote.transpose('M10'))

            # only allow certain melodic intervals
            for cpCurrent in cpNotePoss[cfMeasureNumber - 1]:
                harmIntCurrent = interval.Interval(noteStart=cfNote, noteEnd=cpCurrent)
                for cpPrevious in cpNotePoss[cfMeasureNumber - 2]:
                    harmIntPrevious = interval.Interval(noteStart=cfPrevious, noteEnd=cpPrevious)
                    cfMelodicInterval = interval.Interval(noteStart=cfPrevious, noteEnd=cfNote)
                    cpMelodicInterval = interval.Interval(noteStart=cpPrevious, noteEnd=cpCurrent)

                    if isValidMelodicInterval(cfMelodicInterval) \
                            and isNotForbiddenParallel(harmIntPrevious, harmIntCurrent) \
                            and isNotHiddenParallel(cfMelodicInterval, cpMelodicInterval, harmIntCurrent) \
                            and isNotSimilarSkip(cfMelodicInterval, cpMelodicInterval):
                        cpArrowPoss[cfMeasureNumber - 2].append((cpPrevious, cpCurrent))

        print(cfNote.name + ': ', end='')
        for cpNP in cpNotePoss[cfMeasureNumber - 1]:
            print(cpNP.name + ', ', end='')
        print('===', end=' ')
        if cfMeasureNumber >= 2:
            for cpAP in cpArrowPoss[cfMeasureNumber - 2]:
                print(cpAP[0].name + '->' + cpAP[1].name, end=' ')
        print()

    '''
    # note: need to add an empty measure beforehand, and one after
    for cfmeasure in cfline.getElementsByClass('Measure'):
        cfmeasureNumber = getmeasurenumber(cfmeasure)
        
        cpNotePossibilities[cfmeasureNumber - 1] = []
        cpArrowPossibilities[cfmeasureNumber - 2] = []
        
        if cfmeasureNumber == 1:
            cpNotePossibilities[cfmeasureNumber - 1].append(unison)
            cpNotePossibilities[cfmeasureNumber - 1].append(fifth)
            cpNotePossibilities[cfmeasureNumber - 1].append(octave)
        elif cfmeasureNumber == last:
            cpNotePossibilities[cfmeasureNumber - 1].append(unison)
            cpNotePossibilities[cfmeasureNumber - 1].append(octave)
            
            # only allow melodic steps
            for currentNote in cpNotePossibilities[cfmeasureNumber - 1]:
                for previousNote in cpNotePossibilities[cfmeasureNumber - 2]:
                    if isStep(note1, note2):
                        cpArrowPossibilities[cfmeasureNumber - 2].append((previousNote, currentNote))
            # how to avoid parallel??
            
        else:
            cpNotePossibilities[cfmeasureNumber - 1].append(minor third)
            cpNotePossibilities[cfmeasureNumber - 1].append(major third)
            cpNotePossibilities[cfmeasureNumber - 1].append(fourth)
            cpNotePossibilities[cfmeasureNumber - 1].append(fifth)
            cpNotePossibilities[cfmeasureNumber - 1].append(minor sixth)
            cpNotePossibilities[cfmeasureNumber - 1].append(major sixth)
            cpNotePossibilities[cfmeasureNumber - 1].append(octave)
            cpNotePossibilities[cfmeasureNumber - 1].append(minor tenth)
            cpNotePossibilities[cfmeasureNumber - 1].append(major tenth)
            
            # only allow certain melodic intervals
            for currentNote in cpNotePossibilities[cfmeasureNumber - 1]:
                currentHarmonicInterval = interval(currentCF, currentNote)
                for previousNote in cpNotePossibilities[cfmeasureNumber - 2]:
                    previousHarmonicInterval = interval(previousCF, previousNote)
                    cfMelodicInterval = interval(previousCF, currentCF)
                    cpMelodicInterval = interval(previousNote, currentNote)
                    
                    if isValidMelodicInterval(previousNote, currentNote) 
                    and isNotForbiddenParallel(previousHarmonicInterval, currentHarmonicInterval)
                    and isNotHiddenParallel(cfMelodicInterval, cpMelodicInterval, currentHarmonicInterval)
                    and isNotSimilarSkip(cfMelodicInterval, cpMelodicInterval):
                        cpArrowPossibilities[cfmeasureNumber - 2].append((note1, note2))
            


        cp.append(cpmeasure)
    def isValidMelodicInterval(note1, note2):
        return interval(note1, note2) == 4th, 5th, 8ve, M2, m2, M3, m3, or ascending m6
        
    def isNotForbiddenParallel(prevInt, currInt):
        if prevInt != currInt:
            return true
        else:
            return not currInt in (4th, 5th, 8ve)
            
    def isNotHiddenParallel(cfInt, cpInt, harmInt):
        if harmInt in (5th, 8ve) and direction(cfInt) == direction(cpInt):
            return cfInt == 2nd or cpInt == 2nd
        else:
            return true
            
    def isNotSimilarSkip(cfInt, cpInt):
        return not (cfInt != 2nd and cpInt != 2nd and direction(cfInt) == direction(cpInt))
    
    noteList = []

    for cfmeasure in cf.getElementsByClass('Measure'):
        cpmeasure = stream.Measure()


        cpmeasure.append(note.Note(noteList[i], quarterLength=4))


        cp.append(cpmeasure)
    return cp
    '''

source = converter.parse('cf.mxl')
# source.show('text')

# cantus firmus
cf = source.parts[0]
# print(cf)

# contra punctum
cp = determineFirstSpecies(cf)

'''

# get time signature from cf and add time signature to cp
cp.measure(1).insert(0, cf.flat.getElementsByClass(meter.TimeSignature)[0])

source.insert(0, cp)
'''
# source.show('text')
# source.show()
