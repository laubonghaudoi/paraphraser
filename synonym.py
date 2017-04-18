__author__ = "刘益鸥"
'''
函数：
    coded_synonym() 提取同义词词林，带符号
    uncoded_synonym()   提取同义词词林，无符号
    tag_dictionary(dictionary)  词典中加入词性标签
    cut_tag_sentence(raw_sentence)    句子分词并标注词性
'''

import thulac
cutter = thulac.thulac(seg_only=True)  # Cutter without tagging
cutter_tag = thulac.thulac()  # Cutter with tagging


def coded_synonym():
    '''
    Read the synonym dictionary file and save the synonyms into the list.
    Codes for all the categories are included.

    Return: A list, where every element is a list of synonnyms, where the
            first element is a code for its category.
    '''
    dictionary_file = "./dictionary/Cilin.txt"
    with open(dictionary_file, 'r') as file:
        lines = file.readlines()
        for i in range(len(lines)):
            lines[i] = lines[i].split()
    return lines


def uncoded_synonym():
    '''
    Same as above except codes for all the categories are excluded.

    Return: a list, where every element is a list of synonyms
    '''
    synonym_file = "./dictionary/synonym.txt"
    with open(synonym_file, 'r') as file:
        lines = file.readlines()
        for i in range(len(lines)):
            lines[i] = lines[i].split()
    return lines


def tag_dictionary(dictionary):
    '''
    Add tags to the first column in every line of the synonym dictionary
    '''
    for i in range(len(dictionary)):
        # Label every line
        tense = cutter_tag.cut(dictionary[i][0])
        dictionary[i].insert(0, tense[0][1])


def cut_tag_sentence(raw_sentence):
    '''
    Return: sentence: a list, elements are words
            tags: a list, elements are tags of properties of corresponding words
    '''
    sentence_list = cutter_tag.cut(raw_sentence)

    sentence = []
    for i in range(len(sentence_list)):
        sentence.append(sentence_list[i][0])

    tags = []
    for i in range(len(sentence_list)):
        tags.append(sentence_list[i][1])

    return sentence, tags
