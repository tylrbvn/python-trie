#!/usr/bin/env python
import prefix, suffix, operator, math, itertools, tkFileDialog, tkMessageBox, tkSimpleDialog, ttk
from Tkinter import *
"""-------------------- INTERFACE HELPERS --------------------"""
def loadFile():
    global lexicon
    lexicon = list()
    filename = tkFileDialog.askopenfilename()
    with open(filename) as file:
        for word in file:
            if word not in lexicon:
                lexicon.append(word)
        file.close()
    tkMessageBox.showinfo(app_name, str(len(lexicon)) + ' words loaded!')

def create_trie(start, terminal):
    global trie
    trie = prefix.Tree(start, terminal)
    for word in lexicon:
        trie.insert_word(word.rstrip())
    tkMessageBox.showinfo(app_name, 'Trie successfully created! (' + str(len(trie)) + ' nodes)')

def createTrie():
    d = TrieDialog(root)

def checkAnalogy():
    if len(lexicon) >= 4:
        d = AnalogDialog(root)

def get_analogy(words):
    #Returns dictionary of constituent parts if analogy, else returns None
    words = sorted(words)
    for word1 in words:
        for i in range(len(word1)):
            copy = list(words)
            LHS = word1[:i]
            RHS = word1[i:]
            if LHS != "" and RHS != "":
                copy.remove(word1)
                for word2 in copy:
                    if LHS in word2:
                        RHS2 = word2.split(LHS,1)[1]
                        if RHS2 != "":
                            copy.remove(word2)
                            for word3 in copy:
                                if RHS2 in word3:
                                    LHS2 = word3.split(RHS2,1)[0]
                                    if sorted([LHS + RHS, LHS2 + RHS, LHS + RHS2, LHS2 + RHS2]) == words:
                                        return [[LHS, LHS2], [RHS, RHS2]]
    return None

class TrieDialog(tkSimpleDialog.Dialog):
    def body(self, master):
        Label(master, text="Start symbol (if any):").grid(row=0)
        Label(master, text="Terminal symbol (if any):").grid(row=1)
        self.start = str(Entry(master).grid(row=0, column=1))
        self.terminal = str(Entry(master).grid(row=1, column=1))
        #Initial focus
        return self.start

    def apply(self):
        create_trie(self.start, self.terminal)

class AnalogDialog:
    def __init__(self, parent):
        top = self.top = Toplevel(parent)
        self.no_of_combinations = math.factorial(len(lexicon)) / (24 * math.factorial(len(lexicon) - 4))
        Label(top, text="Check all " + str(self.no_of_combinations) + " possible combinations for analogies?").pack()
        self.progress = ttk.Progressbar(top, orient=HORIZONTAL, length=500, mode='determinate')
        self.progress.pack()
        b = Button(top, text="Start", command=self.ok)
        b.pack(pady=5)

    def ok(self):
        segs = {}
        for word in lexicon:
            segs[word] = list()
        analogy_count = 0
        combi_count = 0
        progress = 0
        for combination in itertools.combinations(lexicon, 4):
            combi_count += 1
            if (combi_count * 100)/self.no_of_combinations > progress:
                progress = (combi_count * 100)/self.no_of_combinations
                self.progress.step()
                self.top.update_idletasks()
            analogy = get_analogy(list(combination))
            if analogy != None:
                analogy_count += 1
                for word in combination:
                    if analogy[0][0] + analogy[1][0] == word or analogy[0][0] + analogy[1][1] == word:
                        index = len(analogy[0][0])
                    else:
                        index = len(analogy[0][1])
                    if index not in segs[word]:
                        segs[word].append(index)
            #print str(combi_count) + " out of " + str(no_of_combinations) + " (" + str((combi_count * 100)/no_of_combinations) + "%) combinations checked"
        ana_count = 0
        for word in lexicon:
            analogy_pos = segs[word]
            ana_count += len(analogy_pos)
        tkMessageBox.showinfo(app_name, str(ana_count) + ' analogies found in the lexicon out of ' + str(self.no_of_combinations) + ' potential combinations!')
        self.top.destroy()

app_name = 'Project'
root = Tk()
root.wm_title(app_name)

# Code to add widgets will go here...
Button(root, text ="Import .txt file", command = loadFile).pack()
Button(root, text ="Generate trie", command = createTrie).pack()
Button(root, text ="Check for analogies", command = checkAnalogy).pack()
root.mainloop()

"""
def create_suffix_tree():
    txt_in = raw_input('Enter name of txt file in dataset folder: ')
    start = raw_input('Enter desired start symbol (if any): ')
    terminal = raw_input('Enter desired terminal symbol (if any): ')
    trie = suffix.Tree(start, terminal)
    with open('dataset/' + txt_in + '.txt') as file:
        for word in file:
            trie.insert_word(word.rstrip())
        file.close()
    print ('\nSuffix tree successfully created! (' + str(len(trie)) + ' nodes)')
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
    graph.layout('dot', args="-Grankdir="+trie.get_graphdir())
    print('Drawing graph...')
    graph.draw('graph/' + png_out + '.png')
    print("Graph '"  + png_out + ".png' successfully exported to graph folder!")

def get_words(trie):
    print trie.get_words()

def print_all_segs(trie):
    words = trie.get_words()
    for word in words:
        print(trie.segment(word))

def export_all_segs(trie):
    txt_out = raw_input('Enter desired name of text file: ')
    file = open('segmentation/' + txt_out + '.txt', 'w')
    words = trie.get_words()
    for word in words:
        file.write(trie.segment(word)+'\n')
    file.close()
    print("List of segmentations '"  + txt_out + ".txt' successfully exported to segmentation folder!")

def get_first_splits(trie):
    first_splits = dict()
    words = trie.get_words()
    for word in words:
        seg = trie.segment(word)
        splits = seg.split("-")
        prefix = splits[0]
        if prefix in first_splits:
            first_splits[prefix] += 1
        else:
            first_splits[prefix] = 1
    first_splits = sorted(first_splits.items(), key=operator.itemgetter(1))
    print(first_splits)

def get_last_splits(trie):
    first_splits = dict()
    words = trie.get_words()
    for word in words:
        seg = trie.segment(word)
        splits = seg.split("-")
        prefix = splits[len(splits)-1]
        if prefix in first_splits:
            first_splits[prefix] += 1
        else:
            first_splits[prefix] = 1
    first_splits = sorted(first_splits.items(), key=operator.itemgetter(1))
    print(first_splits)
"""
