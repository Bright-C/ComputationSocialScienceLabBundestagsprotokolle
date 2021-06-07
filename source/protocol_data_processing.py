from gensim.models import Word2Vec
import nltk
import string
from nltk.corpus import stopwords
import re

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
                    data.protocol_segments[i - 1].text = data.protocol_segments[i - 1].text.rstrip(string.punctuation)

full_punctuation = string.punctuation + "—\n"
translator = str.maketrans(full_punctuation, ' '*len(full_punctuation))

class Word2VecProcessor(ProtocolDataProcessor):
    def process_data(self, data):
        super()
        nltk.download('stopwords')
        full_sentences = re.split("\\.|!|\\?", data.get_full_text())
        # remove single punctuation: "[", "]", ":", "," etc
        
        split_sentences = []
        for sentence in full_sentences:
            sw = stopwords.words("german")
            sentence = sentence.translate(translator)
            sentence_words = sentence.split(" ")
            #sentence_words = [t.translate(translator) for t in sentence_words if t not in sw]
            sentence_words = [t for t in sentence_words if not t.isspace() and len(t) > 0 and t not in sw]
            split_sentences.append(sentence_words)

        model = Word2Vec(sentences = split_sentences)
        model.save("word2vec.model")
