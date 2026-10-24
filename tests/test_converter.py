import unittest

from src.converter import formal_to_slang, slang_to_formal


class ConverterTests(unittest.TestCase):
    def test_formal_to_slang_replaces_long_phrases_and_preserves_punctuation(self):
        self.assertEqual(
            formal_to_slang("I do not know what you are doing right now!"),
            "idk wyd rn!",
        )

    def test_formal_to_slang_is_case_insensitive(self):
        self.assertEqual(formal_to_slang("GOOD MORNING, BEST FRIEND!"), "gm, bestie!")

    def test_formal_to_slang_handles_apostrophes(self):
        self.assertEqual(formal_to_slang("Let's work hard and succeed."), "let's get this bread.")

    def test_formal_to_slang_converts_new_guide_phrases(self):
        self.assertEqual(
            formal_to_slang("That outfit is excellent; I agree."),
            "That outfit slaps; facts.",
        )

    def test_slang_to_formal_converts_new_guide_terms(self):
        self.assertEqual(
            slang_to_formal("Bestie, that fit is fire!"),
            "best friend, that outfit is excellent or cool!",
        )

    def test_multiword_slang_is_matched_before_single_words(self):
        self.assertEqual(slang_to_formal("No cap, let them cook."), "truthfully, let someone continue with their idea.")


if __name__ == "__main__":
    unittest.main()
