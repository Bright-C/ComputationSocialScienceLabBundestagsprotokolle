import re
import datetime
from gensim.models import Word2Vec
from protocol_data import ProtocolData
from collections import defaultdict
from protocol_segments import *
from json_coder_utility import *

class ProtocolReader:
    def get_protocol_data(self, from_file):
        pass

class ProtocolXMLReader(ProtocolReader):
    def __init__(self):
        self.search_date_regex = re.compile("<DATUM>(.*)<\/DATUM>")
        self.search_text_regex = re.compile("<TEXT>((?:.|\s)*)<\/TEXT>")
        self.search_members_pattern = "(.*?)\((.*)\)(?:\.|\s)*\d(?:\.|\s)*[A-Z]"
        self.search_interjection_pattern = "\n\(((?:.|\n)*?)\)\n"
        self.date_format = "%d.%m.%Y"

    def __get_raw_text(self, from_file):
        raw_text = None
        with open(from_file, encoding="UTF-8") as f:
            raw_text = f.read()
        return raw_text

    def get_protocol_data(self, from_file):
        raw_text = self.__get_raw_text(from_file)
        text = self.search_text_regex.search(raw_text).group(1)
        date = self.search_date_regex.search(raw_text).group(1)
        datetime_date = datetime.datetime.strptime(date, self.date_format)

        protocolData = ProtocolData(text, datetime_date)

        for match in re.finditer(self.search_members_pattern, raw_text):
            protocolData.add_member(match.group(1), match.group(2))

        last_match_end = 0
        for match in re.finditer(self.search_interjection_pattern, text):
            protocolData.append_protocol_segment(PureTextSegment(text[last_match_end : match.start()]))
            protocolData.append_protocol_segment(Comment(match.group(1)))
            last_match_end = match.end()
            #protocolData.add_interjection(match.group(1), match.start())

        return protocolData
            
class ProtocolXMLReader2018Up(ProtocolReader):
    def get_protocol_data(self, from_file):
        pass

class ProtocolModelOnlyReader(ProtocolReader):
    def get_protocol_data(self, from_file):
        protocolData = ProtocolData(None, None)
        protocolData.model = Word2Vec.load(from_file)
        return protocolData

class ProtocolJsonOnlyReader(ProtocolReader):
    def get_protocol_data(self, from_file):
        protocolData = ProtocolData(None, None)

        try:
            with open(from_file, "r") as infile:
                word_frequency_data = json.load(infile, cls = WordFrequencyDataJSONDecoder)
        except FileNotFoundError:
            word_frequency_data = WordFrequencyStorageData({}, {})

        all_word_counts = defaultdict(float, word_frequency_data.total_words)
        near_search_word_counts = defaultdict(float, word_frequency_data.words_in_context)
        protocolData.total_searched_words = all_word_counts
        protocolData.most_frequent_words_near_search_words = near_search_word_counts

        return protocolData
