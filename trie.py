#!/usr/bin/env python
import pygraphviz as pgv

class Node:
    def __init__(self, letter=str()):
        self.label = letter
        self.branching_factor = 0
        self.descendants = {}  #Dictionary of descendants
        self.split_point = False

    def __repr__(self):
        """Outputs the branching factor and the dictionary of descendants
        iteratively"""
        string = str(self.branching_factor)
        if (self.split_point):
            string += "-SPLIT"
        string += " " + str(self.descendants)
        return string

    def __len__(self):
        length = 1
        for x in self.descendants:
            length += len(self.descendants[x])
        return length

    def __insert__(self, string, prev_branches = list()):
        letter = string[0]
        #print("Inserting: " + string[0] + " from " + string)
        """-------------------- TRIE BUILDING --------------------"""
        """If the first letter isn't already an immediate descendant of the node
        then create a new node for that letter"""
        if letter not in self.descendants:
            self.descendants[letter] = Node(letter)
            """Trigger update procedure to check if split point"""
            self.branching_factor += 1
            self.split_point = self.__is_split_point__(prev_branches)
            """Also need to now check immediate descendants' updated split point status"""
            for desc in self.descendants:
                self.descendants[desc].split_point = self.descendants[desc].__is_split_point__([self.branching_factor] + prev_branches)

        """If there are remaining characters in the string"""
        if len(string[1:]) > 0:
            """Don't append branching factor of empty root node"""
            if (self.label != ''):
                """Insert the remaining chunk of string below"""
                self.descendants[letter].__insert__(string[1:], [self.branching_factor] + prev_branches)
            else:
                self.descendants[letter].__insert__(string[1:], prev_branches)
            """Trigger update procedure to see if (still) split point"""
            self.split_point = self.__is_split_point__(prev_branches)

    def __is_split_point__(self, prev_branches):
        """Check to the left using list of previous preceeding factors"""
        if (prev_branches):
            p = 0
            while p < len(prev_branches):
                if (self.branching_factor < prev_branches[p]):
                    return False
                elif (self.branching_factor == prev_branches[p]):
                    """Plateau to the left, so keep checking manually"""
                    p += 1
                elif (self.branching_factor > prev_branches[p]):
                    """Check passed to the left, so quit the loop"""
                    break
            """If reached end of preceeding factors without breaking i.e. passing"""
            if (p == len(prev_branches)):
                return False
        else:
            return False

        """Check to the right using dictionary of descendants"""
        if (self.descendants):
            for x in self.descendants:
                if (self.branching_factor < self.descendants[x].branching_factor):
                    return False
                """Pleateau to the right so check recursively"""
                if (self.branching_factor == self.descendants[x].branching_factor):
                    """Special case where in middle of a plateau, therefore not split point"""
                    if (self.branching_factor == prev_branches[0]):
                        return False
                    else:
                        self.split_point = self.descendants[x].__is_split_point__([self.branching_factor] + prev_branches)
            #print(self.label + ' is split point with prev_branches ' + str(prev_branches))
            return True
        else:
            return False

    def __build_graph__(self, graph, terminal, last_key = str()):
        if (self.label):
            """If not first letter or start symbol"""
            if (last_key != ''):
                """Add node, colour code terminals for emphasis"""
                if (self.label == terminal):
                    graph.add_node(last_key + self.label, label = self.label, style = 'filled', fillcolor = 'pink')
                elif (self.split_point):
                    graph.add_node(last_key + self.label, label = self.label, style = 'filled', fillcolor = 'gold')
                else:
                    graph.add_node(last_key + self.label, label = self.label)
                """Add edge"""
                graph.add_edge(last_key, last_key + self.label)
                last_key = last_key + self.label
            else:
                """Add first node"""
                graph.add_node(self.label, label = self.label)
                last_key = self.label

        if (self.descendants):
            for x in self.descendants:
                self.descendants[x].__build_graph__(graph, terminal, last_key)

class Trie:
    def __init__(self, start = str(), terminal = str()):
        self.root = Node()
        self.start = start
        self.terminal = terminal
        self.words = list()
        self.graph = None

    def __repr__(self):
        return str(self.root)

    def __len__(self):
        return len(self.root)

    def insert(self, string):
        self.root.__insert__(string)

    def insert_word(self, word):
        self.words.append(word)
        self.insert(self.start + word + self.terminal)

    def annotate(self, string):
        node = self.root
        annotation = str()
        for x in range(len(string)):
            if string[x] in node.descendants:
                node = node.descendants[string[x]]
                if x > 0:
                    annotation += ", "
                annotation += string[x] + "-" + str(node.branching_factor)
                """Highlight split points"""
                if node.split_point:
                    annotation += "-SPLIT"
            else:
                return None
        return(annotation)

    def annotate_word(self, word):
        return(self.annotate(self.start + word + self.terminal))

    def segment(self, string):
        node = self.root
        segmentation = str()
        for x in range(len(string)):
            if string[x] in node.descendants:
                node = node.descendants[string[x]]
                segmentation += string[x]
                if node.split_point:
                    segmentation += '-'
            else:
                return None
        return segmentation

    def segment_word(self, word):
        return(self.segment(self.start + word + self.terminal)[1:-1])

    def contains(self, string):
        node = self.root
        for letter in string:
            if letter in node.descendants:
                node = node.descendants[letter]
            else:
                return False
        return True

    def contains_word(self, string):
        return self.contains(self.start + string + self.terminal)

    def get_words(self):
        return self.words

    def build_graph(self):
        self.graph = pgv.AGraph(directed=True)
        self.root.__build_graph__(self.graph, self.terminal)

    def get_graph(self):
        return self.graph

"""-------------------- MENU FUNCTIONS --------------------"""
def create_trie():
    txt_in = raw_input('Enter name of txt file in dataset folder: ')
    start = raw_input('Enter desired start symbol (if any): ')
    terminal = raw_input('Enter desired terminal symbol (if any): ')
    trie = Trie(start, terminal)
    with open('dataset/' + txt_in + '.txt') as file:
        for word in file:
            trie.insert_word(word.rstrip())
        file.close()
    print ('\nTrie successfully created! (' + str(len(trie)) + ' nodes)')
    return trie

def annotate_word(trie):
    word = raw_input('Enter word to annotate: ')
    if (trie.contains_word(word)):
        print("Annotation of '" + word + "': " + trie.annotate_word(word))
    else:
        print("Trie does not contain word '" + word + "'!")

def segment_word(trie):
    word = raw_input('Enter word to segment: ')
    if (trie.contains_word(word)):
        print("Segmentation of '" + word + "': " + trie.segment_word(word))
    else:
        print("Trie does not contain word '" + word + "'!")

def contains_word(trie):
    word = raw_input('Enter word to check: ')
    if (trie.contains_word(word)):
        print("Trie contains word '" + word + "'")
    else:
        print("Trie does not contain word '" + word + "'!")

def insert_word(trie):
    word = raw_input('Enter word to insert: ')
    trie.insert_word(word)
    print("Word '" + word + "' successfully inserted!")

def build_graph(trie):
    trie.build_graph()
    print("Graph successfully built!")

def export_graph(trie):
    png_out = raw_input('Enter desired name of png output: ')
    graph = trie.get_graph()
    if not graph:
        print('Building graph first...')
        build_graph(trie)
        graph = trie.get_graph()
    print('Processing graph layout...')
    graph.layout('dot', args="-Grankdir=LR")
    print('Drawing graph...')
    graph.draw('graph/' + png_out + '.png')
    print("Graph '"  + png_out + ".png' successfully exported to graph folder!")

    print("Graph '"  + png_out + ".png' successfully exported to graph folder!")

def get_words(trie):
    print trie.get_words()

def print_all_segs(trie):
    words = trie.get_words()
    for word in words:
        print(trie.segment_word(word))

def export_all_segs(trie):
    txt_out = raw_input('Enter desired name of text file: ')
    file = open('segmentation/' + txt_out + '.txt', 'w')
    words = trie.get_words()
    for word in words:
        file.write(trie.segment_word(word)+'\n')
    file.close()
    print("List of segmentations '"  + txt_out + ".txt' successfully exported to segmentation folder!")

"""-------------------- MENU --------------------"""
print('Welcome! Create a trie from a txt file...\n')
trie = create_trie()
menu = ['Create new trie from txt file', #1
        'Print trie', #2
        'Get node count', #3
        'Insert a word', #4
        'Annotate a word', #5
        'Segment a word', #6
        'Print all word segmentations', #7
        'Export all word segmentations', #8
        'Print list of words in trie', #9
        'Check if trie contains a word', #10
        'Build graph', #11
        'Export graph', #12
        'Exit' #13
        ]
option = 0
while (option != len(menu)):
    print('\n-------------------- MENU --------------------')
    cnt = 0
    for opt in menu:
        cnt += 1
        print(str(cnt) + '. ' + opt)
    option = input('\nEnter option: ')

    if (option == 1): trie = create_trie()
    if (option == 2): print('\nTrie: ' + str(trie))
    if (option == 3): print('Nodes in trie: ' + str(len(trie)))
    if (option == 4): insert_word(trie)
    if (option == 5): annotate_word(trie)
    if (option == 6): segment_word(trie)
    if (option == 7): print_all_segs(trie)
    if (option == 8): export_all_segs(trie)
    if (option == 9): get_words(trie)
    if (option == 10): contains_word(trie)
    if (option == 11): build_graph(trie)
    if (option == 12): export_graph(trie)
    if (option == 13): print('\nGoodbye')
