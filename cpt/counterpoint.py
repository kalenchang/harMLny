from music21 import *

def determineFirstSpecies(cfline):
    cp = stream.Part()
    piano = instrument.Piano()
    cp.insert(0, piano)
    cp.priority = -1
    for cfmeasure in cf.getElementsByClass('Measure'):
        cpmeasure = stream.Measure()


        cpmeasure.append(note.Note(noteList[i], quarterLength=4))


        cp.append(cpmeasure)
    noteList = []

    for cfmeasure in cf.getElementsByClass('Measure'):
        cpmeasure = stream.Measure()


        cpmeasure.append(note.Note(noteList[i], quarterLength=4))


        cp.append(cpmeasure)
    return cp

source = converter.parse('cf.mxl')
# source.show('text')

# cantus firmus
cf = source.parts[0]
# print(cf)

# contra punctum
cp = determineFirstSpecies(cf)

# get time signature from cf and add time signature to cp
cp.measure(1).insert(0, cf.flat.getElementsByClass(meter.TimeSignature)[0])

source.insert(0, cp)

# source.show('text')
source.show()
