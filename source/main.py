#from pdfminer.converter import PDFPageAggregator
#from pdfminer.layout import LAParams, LTTextBox, LTTextLine
#from pdfminer.pdfdocument import PDFDocument
#from pdfminer.pdfinterp import PDFPageInterpreter, PDFResourceManager
#from pdfminer.pdfpage import PDFPage, PDFTextExtractionNotAllowed
#from pdfminer.pdfparser import PDFParser
#import tika
import pandas as pd
import matplotlib.pyplot as plt
import itertools
from protocol_data_readers import *
from protocol_data_processing import *
from gensim import corpora, models, similarities, downloader

xmlReader = ProtocolXMLReader()
wordProcessor = Word2VecProcessor()

data = xmlReader.get_protocol_data("01001.xml")


wordProcessor.process_data(data)

data.print_data()
data.print_data_graph()