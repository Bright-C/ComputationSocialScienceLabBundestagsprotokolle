#from pdfminer.converter import PDFPageAggregator
#from pdfminer.layout import LAParams, LTTextBox, LTTextLine
#from pdfminer.pdfdocument import PDFDocument
#from pdfminer.pdfinterp import PDFPageInterpreter, PDFResourceManager
#from pdfminer.pdfpage import PDFPage, PDFTextExtractionNotAllowed
#from pdfminer.pdfparser import PDFParser
#import tika
import datetime
import re
import pandas as pd
import matplotlib.pyplot as plt
import itertools
from enum import Enum
from gensim import corpora, models, similarities, downloader

xmlReader = ProtocolXMLReader()
wordCounter = CountWordsPrecedingInterjection(200)
wordProcessor = Vector2WordProcessor()

data = xmlReader.get_protocol_data("01001.xml")


wordCounter.process_data(data)
wordProcessor.process_data(data)

data.print_data()
data.print_data_graph()