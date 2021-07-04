from parse_reactions import ReactionParser
import unittest

class TestParseReactions(unittest.TestCase):
    def test_as_reaction_and_performer(self):
        parsed_reaction = ReactionParser.parse_comment("(Beifall bei der CDU/CSU, der SPD, der FDP, der LINKEN und dem BÜNDNIS 90/DIE GRÜNEN – Zuruf der Abg. Beatrix von Storch [AfD])")
        self.assertEqual(parsed_reaction, "COMMENT_BEIFALL_CDU_CSU_FDP_GRUENE_LINKE_SPD COMMENT_ZURUF_AFD")

    def test_as_reaction_and_performer_2(self):
        parsed_reaction = ReactionParser.parse_comment("(Beatrix von Storch [AfD]: Ja, ja!)")
        self.assertEqual(parsed_reaction, "COMMENT_SPEECH_AFD")

    def test_as_reaction_and_performer_3(self):
        parsed_reaction = ReactionParser.parse_comment("Beifall der Abg. Ulli Nissen [SPD]")
        self.assertEqual(parsed_reaction, "COMMENT_BEIFALL_SPD")

    def test_as_reaction_and_performer_4(self):
        parsed_reaction = ReactionParser.parse_comment("(Lachen beim BÜNDNIS 90/DIE GRÜNEN)")
        self.assertEqual(parsed_reaction, "COMMENT_LACHEN_GRUENE")

    def test_as_reaction_and_performer_5(self):
        parsed_reaction = ReactionParser.parse_comment("Die Abgeordneten der  Fraktion  der  LINKEN  halten  Spruchbänder hoch")
        self.assertEqual(parsed_reaction, "COMMENT_UNSPECIFIED_LINKE")

if __name__ == '__main__':
    unittest.main()
