from gensim.models import Word2Vec
import nltk
import string
from nltk.corpus import stopwords
import re
from collections import defaultdict
import json

full_punctuation = string.punctuation + "—\n\t„“"
translator = str.maketrans(full_punctuation, ' '*len(full_punctuation))

class ProtocolDataProcessor:
    def __init__(self):
        pass

    """
        ### Parameters
    1. data : ProtocolData
        - The protocol data to perform processing on. The results of the evaluation should be written back to the object using setters.

    ### Returns
    - void
    """
    def process_data(self, data):
        pass

class CountWordsPrecedingInterjection(ProtocolDataProcessor):
    def __init__(self, neighborhood_character_distance):
        super()
        self.neighborhood_distance = neighborhood_character_distance

    def process_data(self, data):
        for interjection, location in data.interjection_locations.items():
            preceding_neighbor_words = data.text[location - self.neighborhood_distance:location].split()

            for word in preceding_neighbor_words:
                data.count_word_preceding_interjection(word)

class MergeCommentWithPrecedingText(ProtocolDataProcessor):
    def process_data(self, data):
        super()
        for i in range(len(data.protocol_segments)):
            if (type(data.protocol_segments[i]).__name__ == "Comment"):
                if (type(data.protocol_segments[i - 1]).__name__ == "PureTextSegment"):
                    data.protocol_segments[i - 1].text = data.protocol_segments[i - 1].text.rstrip(full_punctuation) + " "

class Word2VecProcessor(ProtocolDataProcessor):
    def process_data(self, data):
        super()
        nltk.download('stopwords')
        full_sentences = re.split("\\.|!|\\?|\t", data.get_full_text())
        # remove single punctuation: "[", "]", ":", "," etc
        
        split_sentences = []
        for sentence in full_sentences:
            sw = stopwords.words("german")
            sentence = sentence.translate(translator)
            sentence_words = sentence.split(" ")
            #sentence_words = [t.translate(translator) for t in sentence_words if t not in sw]
            sentence_words = [t for t in sentence_words if not t.isspace() and len(t) > 0 and t.lower() not in sw]
            if (len(sentence_words) > 0):
                split_sentences.append(sentence_words)

        model = None
        try: 
            model = Word2Vec.load("word2vec.model")
            model.build_vocab(split_sentences, update=True)
            model.train(split_sentences, total_examples=model.corpus_count, epochs=model.epochs)
        except FileNotFoundError:
            model = Word2Vec(sentences = split_sentences)
        
        model.save("word2vec.model")
        print(model.predict_output_word(['COMMENT'], topn = 50))
        data.model = model

class WordFrequencyDataJSONEncoder(json.JSONEncoder):
    def default(self, o):
        return o.__dict__

class WordFrequencyDataJSONDecoder(json.JSONDecoder):
    def decode(self, o):
        result = WordFrequencyStorageData(None, None)
        result.__dict__ = json.loads(o)
        return result

class WordFrequencyStorageData:
    def __init__(self, total_words, words_in_context):
        self.total_words = total_words
        self.words_in_context = words_in_context

class CountRelativeFrequencyOfOtherWordsInSentence(ProtocolDataProcessor):
    def __init__(self, words_to_look_for, permanent_storage):
        super()
        self.words_to_look_for = words_to_look_for
        self.permanent_storage = permanent_storage

    def process_data(self, data):
        super()

        # Debatable whether want to use capitalization or not.
        full_sentences = re.split("\\.|!|\\?|\t", data.get_full_text())
        # remove single punctuation: "[", "]", ":", "," etc
        
        split_sentences = []
        for sentence in full_sentences:
            sw = stopwords.words("german")
            sentence = sentence.translate(translator)
            sentence_words = sentence.split(" ")
            #sentence_words = [t.translate(translator) for t in sentence_words if t not in sw]
            sentence_words = [t for t in sentence_words if not t.isspace() and len(t) > 0 and t.lower() not in sw]
            if (len(sentence_words) > 0):
                split_sentences.append(sentence_words)

        try:
            with open(self.permanent_storage, "r") as infile:
                word_frequency_data = json.load(infile, cls = WordFrequencyDataJSONDecoder)
        except FileNotFoundError:
            word_frequency_data = WordFrequencyStorageData({}, {})

        all_word_counts = defaultdict(float, word_frequency_data.total_words)
        near_search_word_counts = defaultdict(float, word_frequency_data.words_in_context)


        for sentence_words in split_sentences:
            sentence_word_count = defaultdict(float)
            sentence_contained_search_word = False
            for word in sentence_words:
                if word in self.words_to_look_for:
                    sentence_contained_search_word = True
                    continue
                sentence_word_count[word] += 1

            for key, value in sentence_word_count.items():
                all_word_counts[key] += value

                if sentence_contained_search_word:
                    near_search_word_counts[key] += value

        #for word in near_search_word_counts.keys():
        #    near_search_word_counts[word] /= all_word_counts[word]

        sorted_frequencies = dict(sorted(near_search_word_counts.items(), key=lambda x: x[1], reverse=True))
        data.total_searched_words = all_word_counts
        data.most_frequent_words_near_search_words = near_search_word_counts

        with open(self.permanent_storage, "w") as outfile:
            json.dump(WordFrequencyStorageData(all_word_counts, sorted_frequencies), outfile, cls = WordFrequencyDataJSONEncoder, indent = 4)

        print(sorted_frequencies)