#from pdfminer.converter import PDFPageAggregator
#from pdfminer.layout import LAParams, LTTextBox, LTTextLine
#from pdfminer.pdfdocument import PDFDocument
#from pdfminer.pdfinterp import PDFPageInterpreter, PDFResourceManager
#from pdfminer.pdfpage import PDFPage, PDFTextExtractionNotAllowed
#from pdfminer.pdfparser import PDFParser
#import tika
import pandas as pd
import itertools
from protocol_data_readers import *
from protocol_data_processing import *
from gensim import corpora, models, similarities, downloader
from os import listdir
from os.path import isfile, join
protocoldir = "pre2018protocols"
pre2018protocols = [protocoldir + "/" + f for f in listdir(protocoldir) if isfile(join(protocoldir, f))]

xmlReader = ProtocolXMLReader()
commentTextMerger = MergeCommentWithPrecedingText()
relativeFrequencyCounter = CountRelativeFrequencyOfOtherWordsInSentence("COMMENT", "word_frequencies.txt")
w2vProcessor = Word2VecProcessor()

data = None
for protocol in pre2018protocols:
    data = xmlReader.get_protocol_data(protocol)
    commentTextMerger.process_data(data)
    relativeFrequencyCounter.process_data(data)

    #w2vProcessor.process_data(data)
    pass

#modelReader = ProtocolModelOnlyReader()
#data = modelReader.get_protocol_data("word2vec.model")
#data.print_data()
data.print_data_graph()
#print(data.get_full_text())