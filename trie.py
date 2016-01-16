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
        return("Trie contains word '" + string + "': " + str(self.contains(self.start + string + self.terminal)))

    def draw_graph(self, png_name):
        print('Processing graph layout...')
        self.graph.layout('dot', args="-Grankdir=LR")
        print('Drawing graph...')
        self.graph.draw(png_name + '.png')
        print("Graph '"  + png_name + ".png' successfully exported!")

"""-------------------------------- MAIN PROGRAM --------------------------------"""
test_trie = Trie(start = '^', terminal = '$')
txt_in = 'wordlist'
png_out = 'trie'

with open(txt_in + '.txt') as file:
    for word in file:
        test_trie.insert_word(word.rstrip())
    file.close()

test_trie.draw_graph(png_out)
