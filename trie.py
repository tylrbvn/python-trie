class Node:
    def __init__(self, letter=str()):
        self.label = letter
        self.branching_factor = 0
        self.descendants = {}  #Dictionary of descendants
        self.eow = False

    def __insert__(self, word):
        """If the first letter isn't already an immediate descendant of the node
        then create a new node for that letter"""
        letter = word[0]
        if letter not in self.descendants:
            #print('Inserting node ' + letter + ' beneath ' + self.label)
            self.descendants[letter] = Node(letter)
            #print('Updating branching factor of ' + self.label + ' to ' + str(self.branching_factor+1))
            self.branching_factor += 1
        """If there are remaining characters in the word"""
        if len(word[1:]) > 0:
            """Insert the remaining chunk of word below"""
            self.descendants[letter].__insert__(word[1:])
        else:
            self.eow = True

    def __repr__(self):
        """Outputs the branching factor and the dictionary of descendants
        iteratively"""
        return str(self.branching_factor) + " " + str(self.descendants)


class Trie:
    def __init__(self):
        self.root = Node()

    def __repr__(self):
        return str(self.root)

    def insert(self, word):
        self.root.__insert__(word)

    def annotate(self, word):
        node = self.root
        annotation = str()
        for x in range(len(word)):
            if word[x] in node.descendants:
                node = node.descendants[word[x]]
                if x > 0:
                    annotation += "-"
                annotation += word[x] + "/" + str(node.branching_factor)
            else:
                return "String not in trie"
        return annotation

    def contains(self, word):
        node = self.root
        for letter in word:
            if letter in node.descendants:
                node = node.descendants[letter]
            else:
                return False
        return True

"""-------------------------------- MAIN PROGRAM --------------------------------"""
test_trie = Trie()
with open('wordList.txt') as file:
    for word in file:
        test_trie.insert(word.rstrip())
    file.close()
print(test_trie)
print(test_trie.annotate("tea"))
print(test_trie.annotate("in"))
print(test_trie.annotate("true"))
print(test_trie.contains("true"))
print(test_trie.contains("in"))
print(test_trie.contains("t"))

