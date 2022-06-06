from textblob import TextBlob


class SpellChecker:

    def correct(self, text: str) -> str | None:
        corrected_text = str(TextBlob(text).correct())

        return corrected_text
