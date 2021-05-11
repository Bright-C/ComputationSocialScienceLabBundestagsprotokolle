from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBox, LTTextLine
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFPageInterpreter, PDFResourceManager
from pdfminer.pdfpage import PDFPage, PDFTextExtractionNotAllowed
from pdfminer.pdfparser import PDFParser
from tika import parser

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