#!/usr/bin/env python
"""Test script to find the most common prefixes, suffixes and overall segments in sil"""
import prefix, suffix
sil = []

print('Building trie')
#Create tree containing sil words
trie = prefix.Tree("","@")
with open('../dataset/sil.txt') as file:
    for word in file:
        trie.insert_word(word.rstrip())
        sil.append(word.rstrip())
    file.close()

print('Building suffix tree')
#Create suffix tree containing sil words
suffix_tree = suffix.Tree("","@")
with open('dataset/sil.txt') as file:
    for word in file:
        suffix_tree.insert_word(word.rstrip())
    file.close()

prefix_count = 0
suffix_count = 0
joint_count = 0
total_agreements = 0
true_total_agreements = 0

for word in sil:
    #print('Checking ' + word)
    prefix_pos = trie.get_split_point_pos(word)
    suffix_pos = suffix_tree.get_split_point_pos(word)

    prefix_count += len(prefix_pos)
    #print('Adding ' + str(len(prefix_pos)) + ' prefix split points')
    suffix_count += len(suffix_pos)
    #print('Adding ' + str(len(suffix_pos)) + ' suffix split points')
    joint_count += len(set(prefix_pos).intersection(suffix_pos))
    #print('Adding ' + str(len(set(prefix_pos).intersection(suffix_pos))) + ' matching split points')

    if (len(prefix_pos) == len(suffix_pos)) and (len(set(prefix_pos).intersection(suffix_pos)) == len(prefix_pos)):
        total_agreements += 1
        #print('Total agreement word: ' + word)
        if len(prefix_pos)>0:
            true_total_agreements += 1
            print('True total agreement word: ' + word)

print('Prefix tree split points: ' + str(prefix_count))
print('Suffix tree split points: ' + str(suffix_count))
print('Matching split points: ' + str(joint_count))
print('Total agreement words: ' + str(total_agreements))
print('True total agreement words: ' + str(true_total_agreements))
