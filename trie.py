#!/usr/bin/env python
import pygraphviz as pgv

class Node:
    def __init__(self, letter=str()):
        self.label = letter
        self.branching_factor = 0
        self.descendants = {}  #Dictionary of descendants
        self.split_point = False

    def __insert__(self, string, graph, terminal, last_key = str()):
        letter = string[0]

        """-------------------- GRAPH BUILDING --------------------"""
        """If not first letter or start symbol"""
        if (last_key != ''):
            """Add node, colour code s for emphasis"""
            if (letter == terminal):
                graph.add_node(last_key + letter, label = letter, style = 'filled', fillcolor = 'pink')
            else:
                graph.add_node(last_key + letter, label = letter)
            """Add edge"""
            graph.add_edge(last_key, last_key + letter)
            last_key = last_key + letter
        else:
            """Add first node"""
            graph.add_node(letter, label = letter)
            last_key = letter

        """-------------------- TRIE BUILDING --------------------"""
        """If the first letter isn't already an immediate descendant of the node
        then create a new node for that letter"""
        if letter not in self.descendants:
            self.descendants[letter] = Node(letter)
            """Trigger update procedure to check if split_point"""
            self.branching_factor += 1
            if ("""A rule is matched"""):
                self.split_point = True
        """If there are remaining characters in the string"""
        if len(string[1:]) > 0:
            """Insert the remaining chunk of string below"""
            self.descendants[letter].__insert__(string[1:], graph, terminal, last_key)

    def __repr__(self):
        """Outputs the branching factor and the dictionary of descendants
        iteratively"""
        return str(self.branching_factor) + " " + str(self.descendants)

class Trie:
    def __init__(self, start = str(), terminal = str()):
        self.root = Node()
        self.graph = pgv.AGraph(directed=True)
        self.start = start
        self.terminal = terminal

    def __repr__(self):
        return str(self.root)

    def insert(self, string):
        self.root.__insert__(string, self.graph, self.terminal)

    def insert_word(self, word):
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
            else:
                return "String not in trie"
        return("Annotation of '" + string + "': " + annotation)

    def annotate_word(self, word):
        return self.annotate(self.start + word + self.terminal)

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

    def draw_graph(self, png_name):
        print('Processing graph layout...')
        self.graph.layout('dot', args="-Grankdir=LR")
        print('Drawing graph...')
        self.graph.draw(png_name + '.png')

"""-------------------- INTERFACE --------------------"""
def create_trie():
    txt_in = raw_input('Enter name of txt file: ')
    start = raw_input('Enter desired start symbol (if any): ')
    terminal = raw_input('Enter desired terminal symbol (if any): ')
    trie = Trie(start, terminal)
    with open(txt_in + '.txt') as file:
        for word in file:
            trie.insert_word(word.rstrip())
        file.close()
    print ('\nTrie successfully created!')
    return trie

def annotate_word(trie):
    word = raw_input('Enter word to annotate: ')
    print(trie.annotate_word(word))

def contains_word(trie):
    word = raw_input('Enter word to check: ')
    if (trie.contains_word(word)):
        print("Trie contains word '" + word + "'")
    else:
        print("Trie does NOT contain word '" + word + "'")

def export_graph(trie):
    png_out = raw_input('Enter desired name of png output: ')
    trie.draw_graph(png_out)
    print("Graph '"  + png_out + ".png' successfully exported!")

print('Welcome! Create a trie from a txt file...\n')
trie = create_trie()
option = 0
while (option != 6):
    print('\n--- Menu ---\n1. Create new trie from txt file\n2. Print trie\n3. Annotate a word\n4. Check if trie contains a word\n5. Export graph\n6. Exit\n')
    option = input('Enter option: ')
    if (option == 1): trie = create_trie()
    if (option == 2): print('\nTrie: ' + str(trie))
    if (option == 3): annotate_word(trie)
    if (option == 4): contains_word(trie)
    if (option == 5): export_graph(trie)
    if (option == 6): print('\nGoodbye')
