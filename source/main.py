import sys
import pandas as pd
import itertools
from protocol_data_readers import *
from protocol_data_processing import *
from gensim import corpora, models, similarities, downloader
from os import listdir
from os.path import isfile, join
from pathlib import Path

#while len(sys.argv) < 5:
#    sys.argv.append(None)

#sys.argv[1] = "learn"
#sys.argv[2] = "word_frequencies_new.txt"
#sys.argv[3] = ".*COMMENT.*"
#sys.argv[4] = "pre2018protocols"

command = sys.argv[1] # Learn, Count, Predict


data = None
if command == "learn":
    json_in_out_file = sys.argv[2]
    search_pattern = sys.argv[3]
    protocoldir = sys.argv[4]
    pre2018protocols = [protocoldir + "/" + f for f in listdir(protocoldir) if isfile(join(protocoldir, f))]
    commentTextMerger = MergeCommentWithPrecedingText()
    xmlReader = ProtocolXMLReader()

    relativeFrequencyCounter = CountRelativeFrequencyOfOtherWordsInSentence(search_pattern, json_in_out_file)
    for protocol in pre2018protocols:
        data = xmlReader.get_protocol_data(protocol)
        commentTextMerger.process_data(data)
        relativeFrequencyCounter.process_data(data)

    data.plot_significant_words()

elif command == "count":
    json_in_out_file = sys.argv[2]
    search_pattern = sys.argv[3]
    jsonReader = ProtocolJsonOnlyReader()
    data = jsonReader.get_protocol_data(json_in_out_file)
    data.plot_word_count(search_pattern)

elif command == "predict":
    json_in_out_file = sys.argv[2]
    jsonReader = ProtocolJsonOnlyReader()
    data = jsonReader.get_protocol_data(json_in_out_file)
    data.plot_significant_words()

elif command == "preprocess_only":
    protocoldir = sys.argv[2]
    protocols = [protocoldir + "/" + f for f in listdir(protocoldir) if isfile(join(protocoldir, f))]
    commentTextMerger = MergeCommentWithPrecedingText()
    xmlReader = ProtocolXMLReader()

    Path(protocoldir + "/preprocessed").mkdir(parents=True, exist_ok=True)

    for protocol in protocols:
        data = xmlReader.get_protocol_data(protocol)
        commentTextMerger.process_data(data)
        with open(protocol + "_preprocessed.txt", "w", encoding="utf-8") as text_file:
            text_file.write(data.get_full_text())

    

#modelReader = ProtocolModelOnlyReader()
#data = modelReader.get_protocol_data("word2vec.model")
#data.print_data()
#print(data.get_full_text())