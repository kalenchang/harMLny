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

1/4/21
how do we make parse time manageable, given that we have ~3^n (n=# notes) harmonic sentences to parse?
- store constituents across all sentences, instead of just within one parse of a sentence
new parsing plan:
- input: melody notes
- then, for each melody note, get a list of chords which can go with that note (viterbi input)
- then, generate all possible chord progressions (tree traversal) using those chords
- then, look for chromatic chords, and find their constituent dependencies
- then, check if it satisfies FSM
- output: list of chord progressions that match melody and satisfy harmonic rules (viterbi output, but only 1 chord progression)
viterbi alternative:
- instead of generating chords as names (C, D, etc.) generate them as roman numerals (I, ii, etc.) including secondary dominants, etc. like V/V, V/V/V, ...
- then, to calculate transition possibilities (probabilities, but only 1 or 0), just check the "bottom" chord
- - ex. X goes to Y/Z iff X goes to Z. and Y/Z goes to Z ONLY ofc.
- then we can do a full tree traversal of all paths