__author__ = "刘益鸥"
'''
函数：
    read(input_file)    读取句子
    unify_one_sentence(raw_sentence, dictionary)    归一单个句子
    unify_all_sentences(sentences, dictionary)  归一多个句子
'''
# Set up configurations, input and output
from synonym import uncoded_synonym, add_dictionary_tags, cut_tag_sentence

import thulac
cutter = thulac.thulac(seg_only=True)  # Cutter without tagging
cutter_tag = thulac.thulac()  # Cutter with tagging

# Save the paraphrased sentences into output.txt
output_file = "./output/output_unify.txt"
output = open(output_file, 'w')


def read(input_file):
    '''
    Read sentences to be unified.
    '''
    sentences = []
    with open(input_file, 'r') as file:
        lines = file.readlines()

    for i in range(len(lines)):
        if lines[i] != '\n':
            line = cutter.cut(lines[i], text=True).split()
            sentences.append("".join(line))
    return sentences


def unify_one_sentence(raw_sentence, dictionary):
    '''
    加入消歧的同义句归一
    1. 将句子分词
    2. 逐个词语在词林中搜索
    3. 若搜到多个同义词，则先判断是否词性相同
    4. 若还是有多个同义词，则选出最常用的一个意义
    5. 替换此一行的词根
    '''
    sentence, sentence_tags = cut_tag_sentence(raw_sentence)
    # Start unifying, for every word in this sentence
    for w in range(len(sentence)):
        assert len(sentence_tags) == len(sentence)

        meaning = []
        # Traverse the whole synonym dictionary, record all occurance
        for i in range(len(dictionary)):
            if sentence[w] in dictionary[i]:
                meaning.append(i)

        #######################################################################
        # Substitute every word with the base lexicon under hand-designed rules

        n = len(meaning)  # Number of occurance in the dictionary
        # If this word has no synonym
        if n == 0:
            continue  # Next word
        # Only one synonym lexicon
        elif n == 1:
            synonym = dictionary[meaning[0]]  # Only one lexicon, a list
            if sentence_tags[w] != synonym[0]:  # If different property, next
                continue
            else:   # Substitute
                sentence[w] = synonym[1]

        # Multiple synonym lexicons
        else:
            synonyms = []  # Multiple meanings
            for m in meaning:
                if sentence_tags[w] == dictionary[m][0]:
                    synonyms.append(dictionary[m])
            # Now we have a list containing synonyms of the same property

            s = len(synonyms)
            if s == 0:
                continue
            if s == 1:
                synonym = synonyms[0]
                # Substitute
                sentence[w] = synonym[1]
            else:
                idx = []
                for synonym in synonyms:
                    idx.append(synonym.index(sentence[w]))
                assert len(idx) == s
                idx = idx.index(min(idx))
                synonym = synonyms[idx]

                # Substitute
                sentence[w] = synonym[1]

        output.write("".join(sentence) + "\n")


def unify_all_sentences(sentences, dictionary):
    '''
    Unify all sentences in the list and output the processing time
    '''
    import time
    start = time.clock()

    for i in range(len(sentences)):
        unify_one_sentence(sentences[i], dictionary)

    end = time.clock()
    print("Run time: " + str(end - start) + " seconds")


if __name__ == '__main__':
    file = "./output/output.txt"
    sentences = read(file)
    dictionary = uncoded_synonym()
    add_dictionary_tags(dictionary)

    unify_all_sentences(sentences, dictionary)
