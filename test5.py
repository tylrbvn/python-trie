import prefix, suffix, time

def print_timing(func):
    def wrapper(*arg):
        t1 = time.time()
        res = func(*arg)
        t2 = time.time()
        print '%s took %f s' % (func.func_name, (t2-t1))
        return res
    return wrapper

@print_timing
def main(word_limit, mode):
    gold = []
    gold_answers = []

    #Load gold standard answers into structure
    with open('dataset/gold-answers.txt') as file:
        word_count = 0
        for answer in file:
            word_count += 1
            if word_count <= word_limit:
                gold_answers.append(answer.rstrip())
        file.close()

    print('Building trees')
    #Create tree containing gold standard words
    trie = prefix.Tree("^","@")
    suffix_tree = suffix.Tree("^","@")
    with open('dataset/gold.txt') as file:
        word_count = 0
        for word in file:
            word_count += 1
            if word_count <= word_limit:
                #print('Inserting ', word.rstrip())
                trie.insert_word(word.rstrip())
                suffix_tree.insert_word(word.rstrip())
                gold.append(word.rstrip())
        file.close()

    mixed_count = 0
    gold_count = 0
    joint_count = 0

    for i in range(len(gold)):
        #print('Checking ' + gold[i])
        prefix_pos = trie.get_split_point_pos(gold[i])
        #Remove split points at beginning and end of words in trie answers
        for j in range(len(prefix_pos)):
            if prefix_pos[j] == 0 or prefix_pos[j] == len(gold[i]):
                print 'True'
                del prefix_pos[j]
        suffix_pos = suffix_tree.get_split_point_pos(gold[i])
        #Remove split points at beginning and end of words in trie answers
        for j in range(len(suffix_pos)):
            if suffix_pos[j] == 0 or suffix_pos[j] == len(gold[i]):
                del suffix_pos[j]
        #Use to find matching tree split positions
        if mode == 0:
            mixed_pos = set(prefix_pos).intersection(suffix_pos)
        #Use to find ALL tree split points
        else:
            mixed_pos = list(set(prefix_pos + suffix_pos))

        gold_pos = [pos for pos, ltr in enumerate(gold_answers[i]) if ltr == '1']
        #Remove the first and list split points from gold standard answer
        del gold_pos[0]
        del gold_pos[len(gold_pos)-1]

        mixed_count += len(mixed_pos)
        gold_count += len(gold_pos)
        joint_count += len(set(mixed_pos).intersection(gold_pos))

    print 'Mixed tree split points: ' + str(mixed_count)
    #print 'Gold standard split points: ' + str(gold_count)
    print 'Matching split points: ' + str(joint_count)

    precision = float(joint_count)/float(mixed_count)
    recall = float(joint_count)/float(gold_count)

    #print '\n' + 'Precision: ' + str(precision)
    #print 'Recall: ' + str(recall)
    #print 'F score: ' + str(2*(precision*recall)/(precision+recall)) + "\n"

#MODE 0 = MATCHING ONLY, 1 = COMBINE ALL SPLIT POINTS
limit = 25
while limit <= 250:
    print '\n' + str(limit) + ' words'
    main(limit, 0)
    limit += 25
print 'All words'
main(300000, 0)
