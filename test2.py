#!/usr/bin/env python
import prefix, suffix, operator
sil = []

print('Building trie')
#Create tree containing sil words
trie = prefix.Tree("^", "@")
with open('dataset/sil.txt') as file:
    for word in file:
        trie.insert_word(word.rstrip())
        sil.append(word.rstrip())
    file.close()

print('Building suffix tree')
#Create suffix tree containing sil words
suffix_tree = suffix.Tree("^", "@")
with open('dataset/sil.txt') as file:
    for word in file:
        suffix_tree.insert_word(word.rstrip())
    file.close()

prefixes = dict()
suffixes = dict()
all_segments = dict()

for word in sil:
    #TRIE PREFIXES
    seg = trie.segment_word(word)
    splits = seg.split("-")
    prefix = splits[0]
    suffix = splits[len(splits)-1]
    #print(prefix)
    if prefix in prefixes:
        prefixes[prefix] += 1
    else:
        prefixes[prefix] = 1
    if suffix in suffixes:
        suffixes[suffix] += 1
    else:
        suffixes[suffix] = 1

    for segment in splits:
        if segment in all_segments:
            all_segments[segment] += 1
        else:
            all_segments[segment] = 1

    #SUFFIX TREE PREFIXES
    seg = suffix_tree.segment_word(word)
    #print(seg)
    splits = seg.split("-")
    #print(splits)
    prefix = splits[0]
    suffix = splits[len(splits)-1]
    #print(prefix)
    if prefix in prefixes:
        prefixes[prefix] += 1
    else:
        prefixes[prefix] = 1
    if suffix in suffixes:
        suffixes[suffix] += 1
    else:
        suffixes[suffix] = 1

    for segment in splits:
        if segment in all_segments:
            all_segments[segment] += 1
        else:
            all_segments[segment] = 1

combi_prefixes = sorted(prefixes.items(), key=operator.itemgetter(1), reverse=True)
combi_suffixes = sorted(suffixes.items(), key=operator.itemgetter(1), reverse=True)
combi_all = sorted(all_segments.items(), key=operator.itemgetter(1), reverse=True)
print('\nTop 50 combined prefixes: ' + str(combi_prefixes[:50]))
print('\nTop 50 combined suffixes: ' + str(combi_suffixes[:50]))
print('\nTop 50 segments combined: ' + str(combi_all[:50]))

#for pair in combi_prefixes[:100]:
#    print(pair[0] + ',' + str(pair[1]))
