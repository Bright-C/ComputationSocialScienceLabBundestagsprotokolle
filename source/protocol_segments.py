from enum import Enum

class ProtocolSegment:
    """
        Abstract. Classes that represent parts of the protocol should inherit from this and implement get_text_equivalent.
        Sequentially calling get_text_equivalent on all protocol segments should result in a complete protocol.

        ### Returns
        - string
    """
    def get_text_equivalent(self):
        pass

class PureTextSegment(ProtocolSegment):
    def __init__(self, text):
        self.text = text
        self.main_speaker = None
        pass

    def get_text_equivalent(self):
        return self.text
        pass

class CommentType(Enum):
    SPEECH = 0
    BEIFALL = 1
    ZURUF = 2
    LACHEN = 3
    HEITERKEIT = 4

class Comment(ProtocolSegment):
    def __init__(self, text):
        self.comment_type = None
        self.text = text
        self.sentiment = None
        self.main_speaker = None
        self.performers = None
        pass

    def get_text_equivalent(self):
        return "COMMENT. "
        pass
