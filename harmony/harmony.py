from music21 import *
from parser import *

def findChords(melody, scale): # list(note) melody, list(lettername) scale
    chordlist = [] # should contain lists of chords

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
    
    # generate possibilities for chords in between
    for i in range(1, len(melody) - 1):
        chordpossibilities = []
        for eachchord in chordscale:
            if melody[i].name in eachchord[1]:
                chordpossibilities.append(eachchord[2])
        chordlist.append(chordpossibilities)

    # assume end on tonic
    chordlist.append([chordscale[0][2]])

    # create list of possible chord progressions
    paths = [[]]
    for i in range(len(chordlist)):
        # print('melody: ' + melody[i].name + ', chord: ' + str(chordlist[i]))
        updatedpaths = []
        for chordname in chordlist[i]:
            updatedpaths += [path + [chordname] for path in paths]
        paths = updatedpaths

    harmonicgrammar = Grammar(grammarstring)
    harmoniclexicon = Lexicon(lexiconstring)

    i = 0
    validpaths = []
    for path in paths:
        pathchart = Chart(harmoniclexicon, harmonicgrammar, ' '.join(path))
        if pathchart.isvalidchart():
            validpaths.append(path)
            print(path)
        else:
            print('no' + str(i))
            i+=1


    # = stream.Part()
    # piano = instrument.Piano()
    # bass.insert(0, piano)
    # bass.priority = -1

if __name__ == "__main__":

    cmajorscale = ['C3', 'D3', 'E3', 'F3', 'G3', 'A3', 'B3', 'C4', 'D4', 'E4', 'F4']

    source = converter.parse('chorale/Koralmelody.mxl')
    # source.show('text')

    # take melody from mxl file
    mel = source.parts[0]
    # print(mel)
    melnotes = []
    for elem in mel.flat.getElementsByClass(note.Note):
        # print(elem)
        melnotes.append(elem)

    # write bass line
    chords = findChords(melnotes, cmajorscale)

    '''

    # get time signature from cf and add time signature to cp
    cp.measure(1).insert(0, cf.flat.getElementsByClass(meter.TimeSignature)[0])

    source.insert(0, cp)
    '''
    # source.show('text')
    # source.show()
