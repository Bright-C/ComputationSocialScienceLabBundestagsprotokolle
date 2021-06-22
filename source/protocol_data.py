import matplotlib.pyplot as plt
import itertools
plt.rcParams["font.family"] = "Lucida Sans Unicode"

class ProtocolData:
    def __init__(self, text, datetime_date):
        self.date = datetime_date
        self.member_affiliations = {}
        self.text = text
        self.interjection_locations = {}

        self.protocol_segments = []


        # Bit tricky
        self.words_preceding_interjections = {}

    def add_member(self, name, party):
        self.member_affiliations[name] = party

    def append_protocol_segment(self, segment):
        self.protocol_segments.append(segment)

    def count_word_preceding_interjection(self, word):
        self.words_preceding_interjections[word] = self.words_preceding_interjections.get(word, 0) + 1

    def print_data(self):
        print(self.date)
        print(self.member_affiliations)
        print(self.text)
        print(self.interjection_locations)
        print(self.words_preceding_interjections)
        print(len(self.interjection_locations))

    def print_data_graph(self):
        #drawnDict = dict(reversed(sorted(self.words_preceding_interjections.items(), key=lambda item: item[1])))
        #drawnDict = {k: v for k, v in drawnDict.items() if len(k) > 4 or k.isupper()}
        #drawnDict = dict(itertools.islice(drawnDict.items(), 15))
        #prediction = self.model.predict_output_word(['COMMENT'], topn = 20)
        prediction_filtered = [(key, value) for (key, value) in self.most_frequent_words_near_search_words.items() if self.total_searched_words[key] > 3]
        #prediction = list(itertools.islice(self.most_frequent_words_near_search_words.items(), 20))
        prediction = sorted(prediction_filtered[:20], key=lambda x: x[1], reverse=True)
        plt.bar([t[0] for t in prediction], [t[1] for t in prediction])
        #axes = plt.gca()
        #axes.set_ylim([0.011363, 0.011366])
        plt.show()

    def get_full_text(self):
        full_text = ""
        for segment in self.protocol_segments:
            full_text += segment.get_text_equivalent()
        return full_text