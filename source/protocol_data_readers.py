class ProtocolReader:
    def get_protocol_data(self, from_file):
        pass

class ProtocolXMLReader:
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

        for match in re.finditer(self.search_interjection_pattern, text):
            protocolData.add_interjection(match.group(1), match.start())

        return protocolData
            
class ProtocolXMLReader2018Up:
        def get_protocol_data(self, from_file):
            pass
