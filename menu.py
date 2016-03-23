#!/usr/bin/env python
import prefix, suffix, operator
"""-------------------- INTERFACE HELPERS --------------------"""
def create_trie():
    txt_in = raw_input('Enter name of txt file in dataset folder: ')
    start = raw_input('Enter desired start symbol (if any): ')
    terminal = raw_input('Enter desired terminal symbol (if any): ')
    trie = prefix.Tree(start, terminal)
    with open('dataset/' + txt_in + '.txt') as file:
        for word in file:
            trie.insert_word(word.rstrip())
        file.close()
    print ('\nTrie successfully created! (' + str(len(trie)) + ' nodes)')
    return trie

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

"""-------------------- MENU --------------------"""
print('Welcome!')
trie = prefix.Tree()
menu = ['Create new PREFIX tree (trie) from txt file', #1
        'Create new SUFFIX tree from txt file', #2
        'Print trie', #3
        'Get node count', #4
        'Insert a word', #5
        'Annotate a word', #6
        'Segment a word', #7
        'Print all word segmentations', #8
        'Export all word segmentations', #9
        'Print list of words in trie', #10
        'Check if trie contains a word', #11
        'Build graph', #12
        'Export graph', #13
        'Get first splits', #14
        'Get last splits', #15
        'Exit' #16
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
    if (option == 2): trie = create_suffix_tree()
    if (option == 3): print('\nTrie: ' + str(trie))
    if (option == 4): print('Nodes in trie: ' + str(len(trie)))
    if (option == 5): insert_word(trie)
    if (option == 6): annotate_word(trie)
    if (option == 7): segment_word(trie)
    if (option == 8): print_all_segs(trie)
    if (option == 9): export_all_segs(trie)
    if (option == 10): get_words(trie)
    if (option == 11): contains_word(trie)
    if (option == 12): build_graph(trie)
    if (option == 13): export_graph(trie)
    if (option == 14): get_first_splits(trie)
    if (option == 15): get_last_splits(trie)
    if (option == 16): print('\nGoodbye')
