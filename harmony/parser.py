from collections import defaultdict


# Grammar is a collection of rules
class Grammar:

    def __init__(self, rulesinput):
        self.rulelist = []
        for item in rulesinput.split('\n'):
            self.rulelist.append(Rule(item))

    def print(self):
        for rule in self.rulelist:
            rule.print()


# Rule is a rewrite rule, with the nonterminal to be rewritten on the left
# and the nonterminals and terminals (simply called terminals) rewriting on the right
class Rule:

    def __init__(self, stringinput):
        arrowindex = stringinput.index('->')
        self.nonterminal = stringinput[:arrowindex].strip()
        self.terminals = stringinput[arrowindex + 2:].strip().split(' ')
        self.length = len(self.terminals)

    def print(self):
        print(self.nonterminal + ' -> ' + ' '.join(self.terminals))


# Lexicon is a collection of entries of the possible categories of a word
class Lexicon:

    def __init__(self, wordsinput):
        self.entries = defaultdict(list)
        for entry in wordsinput.split('\n'):
            colonindex = entry.index(':')
            self.entries[entry[:colonindex].strip()] = entry[colonindex + 1:].replace(' ', '').split(',')

    def print(self):
        for entry in self.entries:
            print(entry + ' : ' + ', '.join(self.entries[entry]))

    def getentries(self, word):
        return self.entries[word]


# Chart is defined by the lexicon, grammar, and a sentence to be parsed
# it creates a list of constituents, agenda, and arcs
class Chart:

    def __init__(self, lexicon, grammar, sentence):
        self.lexicon = lexicon
        self.grammar = grammar
        self.words = sentence.split(' ')
        self.agenda = []
        self.arcs = []
        self.constituents = []
        self.position = 0

        while self.position < len(self.words):
            self.interpretword()
            while len(self.agenda) > 0:
                self.addconstituent(self.agenda[0])
                self.agenda.pop(0)
            self.position += 1

    def interpretword(self):
        categorylist = self.lexicon.getentries(self.words[self.position])
        for category in categorylist:
            self.agenda.append(Constituent(category, self.position, self.position + 1))

    def addconstituent(self, constituent):
        # add constituent
        self.constituents.append(constituent)

        # add arcs
        for rule in self.grammar.rulelist:
            if constituent.category == rule.terminals[0]:
                self.arcs.append(Arc(rule, constituent.start))

        # advance arcs
        for arc in self.arcs:
            # make sure the constituent is in the right position and the constituent is of the right type
            if constituent.start == arc.current and constituent.category == arc.rule.terminals[arc.positioninrule]:
                if arc.positioninrule == arc.rule.length - 1:
                    self.agenda.append(Constituent(arc.rule.nonterminal, arc.start, arc.current + constituent.length))
                    self.agenda[-1].subconstituents = arc.constituents + [constituent]
                    '''arc.positioninrule += 1
                    arc.current += constituent.length
                    arc.constituents.append(constituent)'''
                else:
                    self.arcs.append(Arc(arc.rule, arc.start, arc.current + constituent.length, arc.positioninrule + 1,
                                     arc.constituents + [constituent]))
        # add completed arcs as constituent

    def printconstituents(self):
        for constituent in self.constituents:
            constituent.print()

    def printarcs(self):
        for arc in self.arcs:
            arc.print()

    def print(self):
        self.printconstituents()
        self.printarcs()
        self.printstructure()

    def printstructure(self, maxwordlength=6):
        for constituent in self.constituents:
            if constituent.category == 'TR' and constituent.start == 0 and constituent.end == len(self.words):
                # constituent.printlayers()
                chartstructure = constituent.returnchart(0, [], maxwordlength)
                for line in chartstructure:
                    print(line)
                for word in self.words:
                    print(word + ' ' * (maxwordlength - len(word)), end=' ')
                print('\n')


# Constituent is an element of the agenda (to be considered) and chart (finalized)
class Constituent:

    def __init__(self, category, startposition, endposition):
        self.category = category
        self.start = startposition
        self.length = endposition - startposition
        self.end = endposition
        self.subconstituents = []

    def print(self):
        print(self.category + ' ' + str(self.start) + ':' + str(self.end))

    def returnchart(self, layer=0, lines=None, maxwordlength=6):
        if lines is None:
            lines = []
        dashlength = (maxwordlength + 1) * (self.end - self.start) - 1 - len(self.category)
        if len(lines) < layer + 1:
            lines.append('')
        while len(lines[layer]) < self.start * (maxwordlength + 1):
            lines[layer] += ' ' * (maxwordlength + 1)
        lines[layer] += self.category + '-' * dashlength + ' '
        for subconstituent in self.subconstituents:
            subconstituent.returnchart(layer + 1, lines)
        if layer == 0:
            return lines

    def printlayers(self):
        self.print()
        for subconstituent in self.subconstituents:
            subconstituent.printlayers()


class Arc:

    def __init__(self, rule, startposition, currentposition=0, positioninrule=0, constituents=None):
        self.rule = rule
        self.start = startposition
        if currentposition == 0:
            self.current = self.start
        else:
            self.current = currentposition
        self.positioninrule = positioninrule
        if constituents is None:
            self.constituents = []
        else:
            self.constituents = constituents

    def print(self):
        print(self.rule.nonterminal + ' -> ' + str(self.start), end=' ')
        for i in range(self.positioninrule):
            print(self.rule.terminals[i], end=' ')
        print(self.current, end=' ')
        for i in range(self.positioninrule, len(self.rule.terminals)):
            print(self.rule.terminals[i], end=' ')
        print('\n', end='')


grammarstring = """TR -> DR t
DR -> SR d
TR -> TR DR
TR -> TR TR
DR -> DR DR
SR -> SR SR
TR -> t
DR -> d
SR -> s"""

lexiconstring = """I : t
IV : s
V : d
ii : s
vi : t
viio : d
C : t, s
D : s, d
E : t
F : s, d
G : t, d
A : s, t
B : d"""

testgrammar = Grammar(grammarstring)
# testgrammar.print()
# print()

testlexicon = Lexicon(lexiconstring)
# testlexicon.print()
# print()

# testsentence = "the old man man the boat on the water"
testsentence = 'E F D C'
testchart = Chart(testlexicon, testgrammar, testsentence)
# testchart.printconstituents()
# print()
testchart.printstructure()

# testsentence = "the old can hold water"
# testchart = Chart(testlexicon, testgrammar, testsentence)
# testchart.printstructure()
