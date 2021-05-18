from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBox, LTTextLine
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFPageInterpreter, PDFResourceManager
from pdfminer.pdfpage import PDFPage, PDFTextExtractionNotAllowed
from pdfminer.pdfparser import PDFParser
from tika import parser
import datetime
import re

def convert_pdf_to_txt(path):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = open(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos=set()

    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)

    text = retstr.getvalue()

    fp.close()
    device.close()
    retstr.close()
    return text

# Source https://stackoverflow.com/questions/26494211/extracting-text-from-a-pdf-file-using-pdfminer-in-python

def pdf2text(path):
    stream = open(path, 'rb')
    parser = PDFParser(stream)
    document = PDFDocument(parser)
    if not document.is_extractable:
        raise PDFTextExtractionNotAllowed

    resmgr = PDFResourceManager()
    laparams = LAParams()
    device = PDFPageAggregator(resmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(resmgr, device)
    for page in PDFPage.create_pages(document):
        interpreter.process_page(page)
        return ''.join([obj.get_text() if hasattr(obj, 'get_text') else '' for obj in device.get_result()])

raw = parser.from_file('first_session.pdf')

# Regex for capturing parliament member affiliations (.*?)\((.*)\)(?:\.|\s)*\d(?:\.|\s)*[A-Z]
print(raw['content'])

class ProtocolXMLReader:
    def __init__(self):
        this.search_date_regex = re.compile("<DATUM>(.*)<\/DATUM>")
        this.search_text_regex = re.compile("<TEXT>(.*)<\/TEXT>")
        this.search_members_pattern = "(.*?)\((.*)\)(?:\.|\s)*\d(?:\.|\s)*[A-Z]"
        this.search_interjection_pattern = "\n\(.*?\)\n"
        this.date_format = "%d.%m.%Y"

    def get_raw_text(self, from_file):
        raw_text = None
        with open(from_file) as f:
            raw_text = f.readlines()
        return raw_text

    def get_protocol_data(self, from_file):
        raw_text = get_raw_text(from_file)
        text = self.search_text_regex.match(raw_text).group(1)
        date = self.search_date_regex.match(raw_text).group(1)
        datetime_date = datetime.datetime.strptime(date, this.date_format)

        protocolData = ProtocolData(text, date, datetime_date)

        for match in re.findall(this.search_members_pattern):
            protocolData.add_member(match.group(1), match.group(2))

        for match in re.findall(this.search_interjection_pattern):
            protocolData.add_interjection(match.group(1))
            


class ProtocolData:
    def __init__(self, text, datetime_date):
        self.date = None
        self.memberAffiliations = {}
        self.text = None
        self.interjections = []

    def add_member(self, name, party):
        memberAffiliations[name] = party

    def add_interjection(self, interjection):
        self.interjections.append(interjection)
