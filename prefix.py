#!/usr/bin/env python
import node, pygraphviz

class Tree:
    def __init__(self, start = str(), terminal = str()):
        self.root = node.Node()
        self.start = start
        self.terminal = terminal
        self.graph = None
        self.graphdir = 'LR'

    def __repr__(self):
        return str(self.root)

    def __len__(self):
        return len(self.root)

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
        for letter in string:
            if letter in node.descendants:
                node = node.descendants[letter]
                segmentation += letter
                if node.split_point:
                    segmentation += '-'
            else:
                return None
        return segmentation

    def get_split_point_pos(self, string):
        word = self.start + string + self.terminal
        node = self.root
        positions = []
        for x in range(len(word)):
            if word[x] in node.descendants:
                node = node.descendants[word[x]]
                if node.split_point:
                    positions.append(x)
            else:
                return None
        return positions

    def segment_word(self, word):
        return self.segment(self.start + word + self.terminal)

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
        self.graph = pygraphviz.AGraph(directed=True)
        self.root.__build_graph__(self.graph, self.terminal)

    def get_words(self):
        return self.root.__get_words_below__(self.terminal)

    def get_words_below(self, path):
        node = self.root
        for letter in path:
            if letter in node.descendants:
                node = node.descendants[letter]
            else:
                return None
        return node.__get_words_below__(self.terminal, path[:-1])

    def get_graph(self):
        return self.graph

    def get_graphdir(self):
        return self.graphdir
