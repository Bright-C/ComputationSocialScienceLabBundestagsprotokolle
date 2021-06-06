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
        self.protocol_segment.append(comment)

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
        drawnDict = dict(reversed(sorted(self.words_preceding_interjections.items(), key=lambda item: item[1])))
        drawnDict = {k: v for k, v in drawnDict.items() if len(k) > 4 or k.isupper()}
        drawnDict = dict(itertools.islice(drawnDict.items(), 15))
        plt.bar(*zip(*drawnDict.items()))
        plt.show()
