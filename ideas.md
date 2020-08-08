# harMLny ideas
## roadmap:
- lit review
    - Kalen
        - Della Ventura
        - Tracy
        - Thorpe
    - Derek
        - Della Ventura
        - Huang et al. (both)
- library review
    - learn music21? seems like most likely candidate
    - read music21 paper/tutorial
- make a list of music rules

- roman numeral analyzer
    - function from melody+accomp
    - to roman numerals

- chord namer
    - given a set of notes,

### derek's approach:

if we build a roman numeral analyzer (melody + accomp -> roman numerals) then, the harmonizer is similar in that it is (melody -> roman numerals), and then we can use the roman numerals to insert chords

here's a problem:
determining harmonic content and harmonic rhythm are dependent of each other

### kalen's approach:

- if you give me a melody (soprano)
- i'll give you chord names (roman numerals)
- AND i'll give you a bass
- if you give S+B
- i'll give you A+T
- now, we have a chorale-maker **but** the harmonic rhythm is fixed at 1 beat (or, whatever the melody beats are)
- so how can we figure out the harmonic rhythm?

notes   G   F   E   D   C
1 beat  I   V   I   V   I
groupingI           V   I
2 beats I       V       I
4 beats V7              I

T                   P   D   T
I                   IV  V   I
IVI     V       I

should we compare the scores of the results of each of the different harmonic rhythms?

constraints that we need to weigh:
- should we preference chord tones, or harmonic function?

ba-charmonizer

take data from existing musical literature (need roman numeral analyzer for that)

- baroque music - things were still kinda modal, and harmonies were viewed on a chord to chord basis more than on a macro-level (cadence), i.e. not really "tonal"
- classical music - rigid adherence to "CPP" harmony rules
- romantic music - expanding harmonic vocabulary, more dissonances
- 20th century - all dissonances or whatever haha it sucks
- jazz
- pop
- jpop - closer to classical music than pop is

we take data from classical music for our harmonizer first. but ideally (after you add appropriate constraints) you can use data from any time period

let's say we assume the harmonic rhythm is 1:
notes   G           F           E           D           C
1 beat  {C,e,G}    {bo,d,F,G7}  {a,C,e}     {G,bo,d}    {F,a,C}
        1,2,3       4,5,6,7     8,9,10
brute force method - algorithmically easy, computationally a disaster (>3^n possibilities)
1   4   8
1   4   9
1   4   10
1   5   8
1   5   9
1   5   10

*use viterbi algorithm*

### 8/3/20
- each write a few melodies, and then both of us harmonize it, explaining our thought process as we do it
- adam neely talks about ai leaving areas blank when it doesn't know what to put there. maybe we could incorporate something like that, i.e. if there's a unit of harmonic rhythm that does not have a clearly winning chord, we just extend the harmony from the previous measure. 
