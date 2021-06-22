from parse_reactions import ReactionParser
import unittest

class TestParseReactions(unittest.TestCase):

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

    def test_as_reaction_and_performer(self):
        parsed_reaction = ReactionParser.parse_comment("(Beifall bei der CDU/CSU, der SPD, der FDP, der LINKEN und dem BÜNDNIS 90/DIE GRÜNEN – Zuruf der Abg. Beatrix von Storch [AfD])")
        self.assertEqual(parsed_reaction, "BEIFALL_CDU_CSU_FDP_GRUENE_LINKE_SPD+ZURUF_AFD")


if __name__ == '__main__':
    unittest.main()
