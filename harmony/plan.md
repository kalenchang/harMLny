some possible goals:
- ~~first species counterpoint~~
- **write a chorale given melody and harmony, and maybe some weighted voice leading constraints**
- determine harmony given a melody, and some weighted harmonic constraints
- determine weights for constraints given a corpus of music

steps:
- given a meldoy
- generate a list of chords that work with each melody note

11/2/20
components:
- chord generator: given a sequence of notes and rhythms (e.g. a measure of melody notes), determine possible chords that fit with those notes and the fitness of the chord
- key relativizer: given chords, determine what functions certain chords can play
- chord parser: given chords/functions, determine valid harmonic structures

possibly combine key relativizer and chord parser