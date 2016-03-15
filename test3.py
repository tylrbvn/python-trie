import prefix, time

def print_timing(func):
    def wrapper(*arg):
        t1 = time.time()
        res = func(*arg)
        t2 = time.time()
        print '%s took %f s' % (func.func_name, (t2-t1))
        return res
    return wrapper

@print_timing
def main(word_limit):
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

    print('Building trie')
    #Create tree containing gold standard words
    trie = prefix.Tree("^","@")
    with open('dataset/gold.txt') as file:
        word_count = 0
        for word in file:
            word_count += 1
            if word_count <= word_limit:
                #print('Inserting ', word.rstrip())
                trie.insert_word(word.rstrip())
                gold.append(word.rstrip())
        file.close()

    trie_count = 0
    gold_count = 0
    joint_count = 0

    for i in range(len(gold)):
        #print('Checking ' + gold[i])
        trie_pos = trie.get_split_point_pos(gold[i])
        gold_pos = [pos for pos, ltr in enumerate(gold_answers[i]) if ltr == '1']
        #Remove the first and list split points from gold standard answer
        del gold_pos[0]
        del gold_pos[len(gold_pos)-1]

        trie_count += len(trie_pos)
        gold_count += len(gold_pos)
        joint_count += len(set(trie_pos).intersection(gold_pos))

    print 'Trie split points: ' + str(trie_count)
    print 'Gold standard split points: ' + str(gold_count)
    print 'Matching split points: ' + str(joint_count)

    precision = float(joint_count)/float(trie_count)
    recall = float(joint_count)/float(gold_count)

    print '\n' + 'Precision: ' + str(precision)
    print 'Recall: ' + str(recall)
    print 'F score: ' + str(2*(precision*recall)/(precision+recall)) + "\n"

maximum = 29827
limit = 75
print str(limit) + ' words'
main(limit)
