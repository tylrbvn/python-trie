#!/usr/bin/env python
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
