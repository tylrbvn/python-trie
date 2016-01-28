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

    def __insert__(self, string, prev_branches = list()):
        letter = string[0]
        """-------------------- TRIE BUILDING --------------------"""
        """If the first letter isn't already an immediate descendant of the node
        then create a new node for that letter"""
        if letter not in self.descendants:
            self.descendants[letter] = Node(letter)
            """Trigger update procedure to check if split_point"""
            self.branching_factor += 1
            self.split_point = self.is_split_point(prev_branches)
            """Also need to now check immediate descendants' updated split point status"""
            for desc in self.descendants:
                self.descendants[desc].split_point = self.descendants[desc].is_split_point([self.branching_factor] + prev_branches)

        """If there are remaining characters in the string"""
        if len(string[1:]) > 0:
            """Insert the remaining chunk of string below"""
            self.descendants[letter].__insert__(string[1:], [self.branching_factor] + prev_branches)

    def is_split_point(self, prev_branches):
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
            """If reached end of preecing factors without breaking i.e. passing"""
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
                        self.split_point = self.descendants[x].is_split_point([self.branching_factor] + prev_branches)
            return True
        else:
            return False

    def build_graph(self, graph, terminal, last_key = str()):
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
                self.descendants[x].build_graph(graph, terminal, last_key)

class Trie:
    def __init__(self, start = str(), terminal = str()):
        self.root = Node()
        self.start = start
        self.terminal = terminal
        self.graph = None

    def __repr__(self):
        return str(self.root)

    def insert(self, string):
        self.root.__insert__(string)

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

    def build_graph(self):
        self.graph = pgv.AGraph(directed=True)
        self.root.build_graph(self.graph, self.terminal)

    def draw_graph(self, png_name):
        if not self.graph:
            print('Building graph first...')
            self.build_graph()
        print('Processing graph layout...')
        self.graph.layout('dot', args="-Grankdir=LR")
        print('Drawing graph...')
        self.graph.draw(png_name + '.png')

"""-------------------- INTERFACE --------------------"""
def create_trie():
    txt_in = raw_input('Enter name of txt file in dataset folder: ')
    start = raw_input('Enter desired start symbol (if any): ')
    terminal = raw_input('Enter desired terminal symbol (if any): ')
    trie = Trie(start, terminal)
    with open('dataset/' + txt_in + '.txt') as file:
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

def insert_word(trie):
    word = raw_input('Enter word to insert: ')
    trie.insert_word(word)
    print("Word '" + word + "' successfully inserted!")

def build_graph(trie):
    trie.build_graph()
    print("Graph successfully built!")

def export_graph(trie):
    png_out = raw_input('Enter desired name of png output: ')
    trie.draw_graph('graph/' + png_out)
    print("Graph '"  + png_out + ".png' successfully exported to graph folder!")

print('Welcome! Create a trie from a txt file...\n')
trie = create_trie()
option = 0
while (option != 8):
    print('\n--- Menu ---\n1. Create new trie from txt file\n2. Print trie\n3. Insert a word\n4. Annotate a word\n5. Check if trie contains a word\n6. Build graph\n7. Export graph\n8. Exit\n')
    option = input('Enter option: ')
    if (option == 1): trie = create_trie()
    if (option == 2): print('\nTrie: ' + str(trie))
    if (option == 3): insert_word(trie)
    if (option == 4): annotate_word(trie)
    if (option == 5): contains_word(trie)
    if (option == 6): build_graph(trie)
    if (option == 7): export_graph(trie)
    if (option == 8): print('\nGoodbye')
