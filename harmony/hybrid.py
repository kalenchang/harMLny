from music21 import *
import diatonicfsm


'''
I: 1 3 5
iii: 3 5 7
S: 1 2 4 6
D: 2 4 5 7
vi: 1 3 6
'''

chordPossDict = {
    1 : ['I', 'S', 'vi'],
    2 : ['S', 'D'],
    3 : ['I', 'iii', 'vi'],
    4 : ['S', 'D'],
    5 : ['I', 'iii', 'D'],
    6 : ['S', 'vi'],
    7 : ['iii', 'D']
}

chromaticScale = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']


def createScaleDict(tonicname):
    tonic = chromaticScale.index(tonicname)
    scaleDict = {
        chromaticScale[tonic] : 1,
        chromaticScale[(tonic + 1) % 12] : 1.5,
        chromaticScale[(tonic + 2) % 12] : 2,
        chromaticScale[(tonic + 3) % 12] : 2.5,
        chromaticScale[(tonic + 4) % 12] : 3,
        chromaticScale[(tonic + 5) % 12] : 4,
        chromaticScale[(tonic + 6) % 12] : 4.5,
        chromaticScale[(tonic + 7) % 12] : 5,
        chromaticScale[(tonic + 8) % 12] : 5.5,
        chromaticScale[(tonic + 9) % 12] : 6,
        chromaticScale[(tonic + 10) % 12] : 6.5,
        chromaticScale[(tonic + 11) % 12] : 7
    }
    return scaleDict


def findChords(melody, tonic): # list(note) melody, str tonic
    
    chordlist = [] # should contain lists of chords
    '''
    tonic = scale[0]
    chordscale = []
    for i in range(7):
        localchord = chord.Chord([scale[i], scale[i+2], scale[i+4]])
        chordscale.append((localchord, [localpitch.name for localpitch in localchord.pitches], localchord.root().name))
        # print(chordscale[i])
        # print(chordscale[i][0].root(), end=' ')
        # print(chordscale[i][0].commonName)
    
    # chordlist is a list that corresponds to each note in the melody. each item of the list is all the possible chords that can go with that melody note
    # assume start on tonic
    chordlist.append([chordscale[0][2]])
    '''


    scaleDict = createScaleDict(tonic)

    # melodyNums = []
    for i in range(0, len(melody)):
        localMelodyNum = scaleDict[melody[i]]
        # melodyNums.append(localMelodyNum)
        if (i == 0) or (i == len(melody) - 1):
            chordlist.append(['I'])
        else:
            chordlist.append(chordPossDict[localMelodyNum])
        

    '''
    # generate possibilities for chords in between
    for i in range(1, len(melody) - 1):
        chordpossibilities = []
        for eachchord in chordscale:
            if melody[i].name in eachchord[1]:
                chordpossibilities.append(eachchord[2])
        chordlist.append(chordpossibilities)

    # assume end on tonic
    chordlist.append([chordscale[0][2]])
    '''

    # create list of possible chord progressions
    paths = [[]]
    for i in range(len(chordlist)):
        # print('melody: ' + melody[i].name + ', chord: ' + str(chordlist[i]))
        updatedpaths = []
        for chordname in chordlist[i]:
            updatedpaths += [path + [chordname] for path in paths]
        paths = updatedpaths



    i = 0
    validpaths = []
    for path in paths:
        if diatonicfsm.check(path):
            validpaths.append(path)
            print(i, end=' ')
            print(path)
            i+=1
    print(i)
    print(len(paths))


    # = stream.Part()
    # piano = instrument.Piano()
    # bass.insert(0, piano)
    # bass.priority = -1

if __name__ == "__main__":

    # cmajorscale = ['C3', 'D3', 'E3', 'F3', 'G3', 'A3', 'B3', 'C4', 'D4', 'E4', 'F4']

    source = converter.parse('chorale/mel221.mxl')
    # source.show('text')

    # take melody from mxl file
    mel = source.parts[0]
    # print(mel)
    melnotes = []
    for elem in mel.flat.getElementsByClass(note.Note):
        # print(elem)
        melnotes.append(elem.name)
    
    print('melody:' + str(melnotes))

    # write bass line
    chords = findChords(melnotes, 'C')

    '''

    # get time signature from cf and add time signature to cp
    cp.measure(1).insert(0, cf.flat.getElementsByClass(meter.TimeSignature)[0])

    source.insert(0, cp)
    '''
    # source.show('text')
    # source.show()
