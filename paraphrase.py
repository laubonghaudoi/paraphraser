__author__ = "刘益鸥"
'''
函数：
    cut_tag_sentence(raw_sentence)    句子分词并标注词性
    paraphrase_one_sentence(raw_sentence, dictionary)    对单句进行同义词替换
    paraphrase_all_sentences(sentences, dictionary)  对一列表句子进行同义句替换
    read_output() 读取输出的句子进行复合替换
'''

# Set up configurations, input and output
from synonym import uncoded_synonym, tag_dictionary, cut_tag_sentence

# Prepare the sentece cutters, with and without part-of-speech tagging.
import thulac
cutter = thulac.thulac(seg_only=True)  # Cutter without tagging
cutter_tag = thulac.thulac()  # Cutter with tagging

sentences = ["帮我订张机票",
             "丹霞山在哪里？",
             "白云山有多高？",
             "明天天气如何？",
             "峨眉山有多大面积？"]

# Save the paraphrased sentences into output.txt
output_file = "./output/output.txt"
output = open(output_file, 'w')


def paraphrase_one_sentence(raw_sentence, dictionary):
    '''
    加入消歧的同义句生成
    1. 将句子分词
    2. 逐个词语在词林中搜索
    3. 若搜到多个同义词，则先判断是否词性相同
    4. 若还是有多个同义词，则选出最常用的一个词义
    5. 替换此词义同一行的全部词语
    '''
    # We first get the tag of every word in the sentence
    sentence, sentence_tags = cut_tag_sentence(raw_sentence)

    # Start paraphasing, for every word in this sentence
    for w in range(len(sentence)):
        assert len(sentence_tags) == len(sentence)
        meaning = []
        # Traverse the whole synonym dictionary, record all occurance
        for i in range(len(dictionary)):
            if sentence[w] in dictionary[i]:
                meaning.append(i)

        #######################################################################
        # Substitute words under hand-designed rules

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
                left = sentence[:w]
                right = sentence[w + 1:]
                for syn in synonym:
                    if syn != synonym[0]:
                        output.write("".join(left + [syn] + right))
                        output.write("\n")
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
                left = sentence[:w]
                right = sentence[w + 1:]
                for syn in synonym:
                    if syn != synonym[0]:
                        output.write("".join(left + [syn] + right))
                        output.write("\n")
            else:
                idx = []
                for synonym in synonyms:
                    idx.append(synonym.index(sentence[w]))
                assert len(idx) == s
                idx = idx.index(min(idx))
                synonym = synonyms[idx]

                # Substitute
                left = sentence[:w]
                right = sentence[w + 1:]
                for syn in synonym:
                    if syn != synonym[0]:
                        output.write("".join(left + [syn] + right))
                        output.write("\n")


def paraphrase_all_sentences(sentences, dictionary):
    '''
    Paraphase all sentences in the list and print the processing time.
    Output sentences are written into output_file
    '''
    import time
    start = time.clock()

    for i in range(len(sentences)):
        paraphrase_one_sentence(sentences[i], dictionary)

    end = time.clock()
    print("Run time: " + str(end - start) + " seconds")


def read_output():
    '''
    Read output.txt as input sentences.

    Return: a list of sentences
    '''
    sentences = []
    with open(output_file, 'r') as file:
        lines = file.readlines()

    for i in range(len(lines)):
        if lines[i] != '\n':
            line = cutter.cut(lines[i], text=True).split()
            sentences.append("".join(line))
    return sentences


if __name__ == '__main__':
    dictionary = uncoded_synonym()
    tag_dictionary(dictionary)
    paraphrase_all_sentences(sentences, dictionary)

    # Reparaphrase sentences
    sentences = read_output()
    paraphrase_all_sentences(sentences, dictionary)
