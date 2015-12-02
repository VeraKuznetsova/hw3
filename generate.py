import sys
import random
import string
from statistic import Statistic
import json


class EndOfTextError(Exception):
    def __str__(self):
        return "The word has no word after it"


class TextGenerator(object):
    def __init__(self, statistic, text_len, line_len, sentences_in_paragraph):
        self.statistic = statistic
        self.words_to_generate = text_len
        self.line_len = line_len
        self.sentences_in_paragraph = sentences_in_paragraph
        self.first_word = ''
        self.second_word = ''
        self.current_line_len = 0

    def gen(self):
        text = []
        try:
            while self.words_to_generate > 0:
                paragraph = self.generate_paragraph()
                text.extend(paragraph)
        except EndOfTextError:
            pass
        finally:
            return ' '.join(text).replace('\n ', '\n')

    def generate_paragraph(self):
        text = []
        sentences_count = 0
        while (sentences_count < sentences_in_paragraph and
               self.words_to_generate > 0):
            sentence = self.generate_sentence()
            text.extend(sentence)
            sentences_count += 1
            self.words_to_generate -= len(sentence)
        text[len(text) - 1] += '\n\n'
        self.current_line_len = 0
        return text

    def generate_sentence(self):
        text = []
        third_word = self.generate_word()
        text.append(third_word.capitalize())
        self.first_word = self.second_word
        self.second_word = third_word
        self.current_line_len += len(third_word)
        while third_word not in {'.', '!', '?'}:
            third_word = self.generate_word()
            self.first_word = self.second_word
            self.second_word = third_word
            if (self.current_line_len >= self.line_len and
                    third_word not in string.punctuation):
                text[len(text) - 1] += '\n'
                self.current_line_len = 0
            self.current_line_len += len(third_word)
            if third_word in string.punctuation and third_word != '-':
                text[len(text) - 1] += third_word
            else:
                text.append(third_word)
        return text

    def generate_word(self):
        if self.second_word == '':
            counter = statistic.words_counter
        elif self.first_word == '':
            counter = statistic.pairs_dictionary[self.second_word]
        else:
            counter = statistic.triplets_dictionary[self.first_word +
                                                    ' ' + self.second_word]
        word = self.next_word(counter)
        return word

    def next_word(self, words_counter):
        if len(words_counter) == 0:
            raise EndOfTextError()
        value = random.randrange(sum(words_counter.values()))
        freq_sum = 0
        for item in words_counter.items():
            freq_sum += item[1]
            if freq_sum >= value:
                return item[0]


if __name__ == '__main__':
    statistic_dir = sys.argv[1]

    with open(statistic_dir + "\words.txt") as input_file:
        words_counter = json.load(input_file)
    with open(statistic_dir + "\pairs.txt") as input_file:
        pairs_dictionary = json.load(input_file)
    with open(statistic_dir + "\\triplets.txt") as input_file:
        triplets_dictionary = json.load(input_file)

    statistic = Statistic(words_counter, pairs_dictionary, triplets_dictionary)

    text_len = int(sys.argv[2])
    line_len = int(sys.argv[3])
    sentences_in_paragraph = int(sys.argv[4])

    generator = TextGenerator(statistic,
                              text_len,
                              line_len,
                              sentences_in_paragraph)
    text = generator.gen()
    print text
