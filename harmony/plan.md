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
- output: list of chord progressions that match melody and satisfy harmonic rules (v iterbi output, but only 1 chord progression)
viterbi alternative:
- instead of generating chords as names (C, D, etc.) generate them as roman numerals (I, ii, etc.) including secondary dominants, etc. like V/V, V/V/V, ...
- then, to calculate transition possibilities (probabilities, but only 1 or 0), just check the "bottom" chord
  - ex. X goes to Y/Z iff X goes to Z. and Y/Z goes to Z ONLY ofc.
- then we can do a full tree traversal of all paths

1/21/21
- potential problem with above parsing plan:
  - what if you have a chord before a tonicized phrase that is diatonic in both the original key and tonicized key, but it is ungrammatical in that position in the original key
- what if we used something that's not python to be faster (or just use diff interpreter)
- context change idea:
  - based on Tymoczko's markov model based theory, except incorporating aspects of a hierarchical model - every "context" (eg a key) has its own probability matrix, and each context's matrix also contains probabilities for moving to other contexts. in theory this allows for generating hierarchical structures like secondary dominants and tonicizations using the markov model theory, which Tymoczko's original theory does not support.
  - some problems for this: see whiteboard 1/21

2/18/21
possible implementations:
1. original plan: full hierarchical structure parser (based on parser of natural language) -- too slow
2. hybrid approach: non-diatonic chords are first checked for dependencies then resolved (deleted). remaining diatonic chords are checked against a FSM
3. viterbi approach: first try viterbi on diatonic chords. then to implement secondary dominants, etc. add either a "gap" or something like that... like V/V serves as a V chord from the front (anything that can go to V can go to V/V) but leads to a V chord in the back
4. context changes (see 1/21/21 above)
progress today:
- started implementing hybrid approach
- finished the diatonic chord checker/fsm
- need to fix chord generation in hybrid.py so that we can generate non-diatonic chords
- then check for dependencies of non-diatonic chords :)
we should also listen to a bunch of harmonizations and see what sounds "good" and what doesn't:
- ex. alternating between 2 and 4 (or any two chords) too much is bad, maybe should only be one way
- 4 - 1 alternation too much is also bad, maybe only for certain cadences or something
- too many repeated chords bad
- too many bdim chords bad
- etc

2/27/21
- note for kalen: melody d to e (causes melodic/harmonic clashes)
- fixed chord generation so it is based on scale degrees and roman numerals
- grouped together ii/IV into S and V/viio into D
- need to do:
  - after scoring, create a disambiguator for the S chords and the D chords
  - disambiguate with both melodic and harmonic cues. should be no harmonic/harmonic clashes, only melodic/harmonic clashes
  - add non-diatonic chords!

3/11/21
- pre-disambiguation scoring
  - avoid too many repeated chords in a row
  - avoid alternating between the same 2 chords
  - cadences (at least end V-I)
- biases from random assignment:
  - prefer V over viio
  - 50/50 ii IV
  - can adjust probabilities after we introduce more chords (V7, ii7, V/V, etc.)
- next time: implement pre-disambiguation scoring


4/24/21
- what we did today
  - finished diatonic viterbi
  - right now it can generate sequences of chords, but they are usually the most common, hard to get the uncommon chords
  - can have lots of repetition/alternating between chords bc of insufficient (long-term) memory
- idea for future
  - check how viterbi performs with 3-grams
  - would need to generate or collect data
- what we want to think about
  - can viterbi be sufficient for what we want? i.e. if we extend it
  - can we somehow get, like, the 5 highest scoring paths in viterbi somehow (not exactly top 5, but close)
    - if so, then we can independently rank them without short-term memory constraints
    - what if we introduced a random number, e.g. multiply/add transition probabilites or tr_prob by random numbers, which may change the overall outcome
  - implement derek's tonicization idea (1/21/21)
  - what if we simplified the contexts even more, to only I/ii/V/vi maybe, and to get anything else you have to context change (e.g. iii is ii/ii)
  - would be interesting to compare viterbi w context changing to hierarchical fsms

6/4/21
- last week we talked about: parsing
- top-down vs bottom-up vs other approaches, etc.
- the problem we are facing is not that parsing is slow, it's that we have too many possibilities
- as the melody gets longer, the number of valid parses increases (exponentially?) and the number of parses we have to parse AND rank later on increases
- so the problem isnt necessarily parsing faster, but to reduce the number of valid parses somehow
- some theoretical approaches:
  - constrain the grammar (reduce number of parses)
  - use t s d instead of numbers
  - break down the melody into subphrases which are sequences of tsdt
    - eg. ii-IV alternation for s happens locally within tsd phrase (the reason we get exponential possibilities is because ii-IV alternation possible for each tsd)
- some engineering approaches:
  - introduce randomness (could be informed randomness)
  - limit the melody to a certain length
  - randomly eliminate 1/2 or so of the parses, or just randomly select 100 to evaluate and rank
  - modified viterbi: (random)
    - instead of choosing the chord with highest probability/score at each step, you just generate all valid (p > 0) transitions, and then at the end, randomly choose a sequence of transitions that works (or 100) (see fig 1). need to prune dead-ends from the back before beginning
    - ~~or: we just run the normal viterbi algorithm but instead of choosing the highest prob at each point, just choose a random one~~
      - doesn't work because viterbi does not choose at each point, it creates chains of prevs to the end, and at that point it chooses one path
- some areas to reduce size of problem:
  - some parses are minimally similar. eg. I IV V I vs I ii V I
- idea for future: cadences

```
fig. 1
(1, 2, 3) x (4, 5, 6) x (7, 8, 9) x ... n times
3^n sequences
3^2 * (n-1) transitions
```

6/18/21
- 