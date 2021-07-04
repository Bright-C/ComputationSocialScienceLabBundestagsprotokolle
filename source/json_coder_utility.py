import json

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
