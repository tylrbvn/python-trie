#!/usr/bin/env python
import node, pygraphviz

class Tree:
    def __init__(self, start = str(), terminal = str()):
        self.root = node.Node()
        self.start = start
        self.terminal = terminal
        self.words = list()
        self.graph = None
        self.graphdir = 'LR'

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
        segmentation = self.segment(self.start + word + self.terminal)
        #Cut off start and terminal symbols
        if (segmentation[0] == self.start):
            segmentation = segmentation[1:]
        if (segmentation[len(segmentation)-1] == (self.terminal)):
            segmentation = segmentation[:-1]
        return(segmentation)

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
        self.graph = pygraphviz.AGraph(directed=True)
        self.root.__build_graph__(self.graph, self.terminal)

    def get_graph(self):
        return self.graph

    def get_graphdir(self):
        return self.graphdir
