import sys
import re
import collections
import os
import json


alphabet = re.compile(u'[a-zA-Z0-9-\']+|[.,:;?!]+')


class Statistic(object):
    def __init__(self, words_counter, pairs_dictionary, triplets_dictionary):
        self.words_counter = words_counter
        self.pairs_dictionary = pairs_dictionary
        self.triplets_dictionary = triplets_dictionary


class StatisticGenerator(object):
    def __init__(self, corpus):
        self.corpus = corpus

    def generate_statictic(self):
        words_counter = collections.Counter(self.first_words())

        pairs_dictionary = collections.defaultdict(collections.Counter)
        for pair in self.pairs():
            pairs_dictionary[pair[0]].update([pair[1]])

        triplets_dictionary = collections.defaultdict(collections.Counter)
        for triplet in self.triplets():
            triplets_dictionary[triplet[0] + ' ' +
                                triplet[1]].update([triplet[2]])

        return Statistic(words_counter, pairs_dictionary, triplets_dictionary)

    def first_words(self):
        prev_word = '.'
        for word in self.corpus:
            if prev_word in {'.', '!', '?'}:
                yield word
            prev_word = word

    def pairs(self):
        first_word = ''
        for second_word in self.corpus:
            if first_word != '':
                yield first_word, second_word
            first_word = second_word

    def triplets(self):
        first_word = ''
        second_word = ''
        for third_word in self.corpus:
            if second_word != '':
                yield first_word, second_word, third_word
            first_word = second_word
            second_word = third_word


if __name__ == '__main__':
    directory = sys.argv[1]
    corpus = []
    for (dirpath, dirnames, filenames) in os.walk(directory):
        for filename in filenames:
            with open(dirpath + "\\" + filename) as input_file:
                for line in input_file.xreadlines():
                    words = alphabet.findall(line.lower())
                    corpus.extend(words)

    generator = StatisticGenerator(corpus)
    statistic = generator.generate_statictic()

    statistic_dir = sys.argv[2]
    with open(statistic_dir + "\words.txt", 'wb') as output_file:
        json.dump(statistic.words_counter, output_file)
    with open(statistic_dir + "\pairs.txt", 'wb') as output_file:
        json.dump(statistic.pairs_dictionary, output_file)
    with open(statistic_dir + "\\triplets.txt", 'wb') as output_file:
        json.dump(statistic.triplets_dictionary, output_file)
