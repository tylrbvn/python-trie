#!/usr/bin/env python
import Trie
"""--------------------TERMINAL INTERFACE --------------------"""
def create_trie():
    txt_in = raw_input('Enter name of txt file in dataset folder: ')
    start = raw_input('Enter desired start symbol (if any): ')
    terminal = raw_input('Enter desired terminal symbol (if any): ')
    trie = Trie.Trie(start, terminal)
    with open('dataset/' + txt_in + '.txt') as file:
        for word in file:
            trie.insert_word(word.rstrip())
        file.close()
    print ('\nTrie successfully created! (' + str(len(trie)) + ' nodes)')
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
    graph.layout('dot', args="-Grankdir=LR")
    print('Drawing graph...')
    graph.draw('graph/' + png_out + '.png')
    print("Graph '"  + png_out + ".png' successfully exported to graph folder!")

def get_words(trie):
    print trie.get_words()

def print_all_segs(trie):
    words = trie.get_words()
    for word in words:
        print(trie.segment_word(word))

def export_all_segs(trie):
    txt_out = raw_input('Enter desired name of text file: ')
    file = open('segmentation/' + txt_out + '.txt', 'w')
    words = trie.get_words()
    for word in words:
        file.write(trie.segment_word(word)+'\n')
    file.close()
    print("List of segmentations '"  + txt_out + ".txt' successfully exported to segmentation folder!")

"""-------------------- MENU --------------------"""
print('Welcome! Create a trie from a txt file...\n')
trie = create_trie()
menu = ['Create new trie from txt file', #1
        'Print trie', #2
        'Get node count', #3
        'Insert a word', #4
        'Annotate a word', #5
        'Segment a word', #6
        'Print all word segmentations', #7
        'Export all word segmentations', #8
        'Print list of words in trie', #9
        'Check if trie contains a word', #10
        'Build graph', #11
        'Export graph', #12
        'Exit' #13
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
    if (option == 2): print('\nTrie: ' + str(trie))
    if (option == 3): print('Nodes in trie: ' + str(len(trie)))
    if (option == 4): insert_word(trie)
    if (option == 5): annotate_word(trie)
    if (option == 6): segment_word(trie)
    if (option == 7): print_all_segs(trie)
    if (option == 8): export_all_segs(trie)
    if (option == 9): get_words(trie)
    if (option == 10): contains_word(trie)
    if (option == 11): build_graph(trie)
    if (option == 12): export_graph(trie)
    if (option == 13): print('\nGoodbye')
