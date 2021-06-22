from parse_reactions import ReactionParser
import unittest

class TestParseReactions(unittest.TestCase):
    def test_as_reaction_and_performer(self):
        parsed_reaction = ReactionParser.parse_comment("(Beifall bei der CDU/CSU, der SPD, der FDP, der LINKEN und dem BÜNDNIS 90/DIE GRÜNEN – Zuruf der Abg. Beatrix von Storch [AfD])")
        self.assertEqual(parsed_reaction, "BEIFALL_CDU_CSU_FDP_GRUENE_LINKE_SPD ZURUF_AFD")


if __name__ == '__main__':
    unittest.main()
