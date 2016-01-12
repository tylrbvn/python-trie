class Node:
    def __init__(self, letter=str()):
        self.label = letter
        self.branching_factor = 0
        self.descendants = {}  #Dictionary of descendants

    def __insert__(self, string):
        """If the first letter isn't already an immediate descendant of the node
        then create a new node for that letter"""
        letter = string[0]
        if letter not in self.descendants:
            self.descendants[letter] = Node(letter)
            """Update branching factor if not inserting terminal symbol"""
            if letter != "$":
                self.branching_factor += 1
        """If there are remaining characters in the string"""
        if len(string[1:]) > 0:
            """Insert the remaining chunk of string below"""
            self.descendants[letter].__insert__(string[1:])

    def __repr__(self):
        """Outputs the branching factor and the dictionary of descendants
        iteratively"""
        return str(self.branching_factor) + " " + str(self.descendants)


class Trie:
    def __init__(self):
        self.root = Node()

    def __repr__(self):
        return str(self.root)

    def insert(self, string):
        self.root.__insert__(string)

    def annotate(self, string):
        node = self.root
        annotation = str()
        for x in range(len(string)):
            if string[x] in node.descendants:
                node = node.descendants[string[x]]
                if x > 0:
                    annotation += "-"
                annotation += string[x] + "/" + str(node.branching_factor)
            else:
                return "String not in trie"
        return annotation

    def contains_string(self, string):
        node = self.root
        for letter in string:
            if letter in node.descendants:
                node = node.descendants[letter]
            else:
                return False
        return True

    def contains_word(self, string):
        return(self.contains_string(string + "$"))

"""-------------------------------- MAIN PROGRAM --------------------------------"""
test_trie = Trie()

with open('wordList.txt') as file:
    for word in file:
        test_trie.insert(word.rstrip() + "$")
    file.close()

print(test_trie)
print(test_trie.contains_word("work"))
print(test_trie.contains_word("working"))
print(test_trie.contains_word("bake"))
print(test_trie.contains_word("baking"))
print(test_trie.annotate("bake"))
print(test_trie.contains_word("shake"))
print(test_trie.contains_word("shaking"))
