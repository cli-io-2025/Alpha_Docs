"""
pyspell_integration.py — Enterprise Spell Checking Engine
Real-time spell checking, squiggly wave underline syntax highlighter,
dictionary lookup, and user custom dictionary additions.
"""
import os
import re

try:
    from symspellpy import SymSpell, Verbosity
    HAS_SPELL = True
except ImportError:
    HAS_SPELL = False


class SpellChecker:
    """Wrapper for PySpell (symspellpy) integration with custom dictionary support."""

    def __init__(self):
        self.sym_spell = None
        self.is_ready = False
        self.user_dictionary = set()

        if HAS_SPELL:
            try:
                self.sym_spell = SymSpell(max_dictionary_edit_distance=2, prefix_length=7)
                import symspellpy
                dict_path = os.path.join(os.path.dirname(symspellpy.__file__), "frequency_dictionary_en_82_765.txt")
                if os.path.exists(dict_path):
                    self.sym_spell.load_dictionary(dict_path, term_index=0, count_index=1)
                    self.is_ready = True
                else:
                    print(f"[SpellChecker] Dictionary file not found at {dict_path}")
            except Exception as e:
                print(f"[SpellChecker] Failed to load symspellpy dictionary: {e}")

    def add_to_dictionary(self, word: str):
        """Adds a word to the active user session dictionary."""
        cleaned = word.strip().lower()
        if cleaned:
            self.user_dictionary.add(cleaned)
            if self.is_ready and self.sym_spell:
                try:
                    self.sym_spell.create_dictionary_entry(cleaned, 1000)
                except Exception:
                    pass

    def get_misspellings(self, text: str) -> list[tuple[str, str, int]]:
        """
        Check text and return a list of misspelled words along with their top suggestion.
        Returns: list of (original_word, suggestion, position_index)
        """
        if not self.is_ready or not text:
            return []

        misspellings = []
        for match in re.finditer(r"\b[a-zA-Z]+(?:'[a-zA-Z]+)?\b", text):
            word = match.group(0)

            # Skip acronyms / uppercase words of 2+ chars
            if word.isupper() and len(word) > 1:
                continue

            # Skip user dictionary words
            if word.lower() in self.user_dictionary:
                continue

            try:
                suggestions = self.sym_spell.lookup(
                    word,
                    Verbosity.CLOSEST,
                    max_edit_distance=2,
                    include_unknown=False
                )
                if suggestions:
                    best = suggestions[0].term
                    # If best match differs from word (case-insensitive check)
                    if best.lower() != word.lower():
                        # Preserve original capitalization style
                        if word.istitle():
                            best = best.capitalize()
                        elif word.isupper():
                            best = best.upper()
                        misspellings.append((word, best, match.start()))
                else:
                    # Word not in dictionary and no suggestion found
                    misspellings.append((word, "", match.start()))
            except Exception:
                pass

        return misspellings

    def get_word_at_pos(self, text: str, pos: int) -> tuple[str, str, int] | None:
        """Returns (word, suggestion, start_pos) if word at pos is misspelled."""
        for orig, sugg, start in self.get_misspellings(text):
            if start <= pos <= start + len(orig):
                return orig, sugg, start
        return None

    def correct_text(self, text: str) -> str:
        """Replaces all misspelled words in the text with top suggestions."""
        misspellings = self.get_misspellings(text)
        corrected_text = text
        for orig, sugg, pos in reversed(misspellings):
            if sugg:
                corrected_text = corrected_text[:pos] + sugg + corrected_text[pos + len(orig):]
        return corrected_text


# Initialize a global/shared instance for highlighters to use easily
_shared_checker = None

def get_shared_checker() -> SpellChecker:
    global _shared_checker
    if _shared_checker is None:
        _shared_checker = SpellChecker()
    return _shared_checker


try:
    from PySide6.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor, QTextDocument
    from PySide6.QtCore import Qt
    HAS_QT_SPELL = True
except ImportError:
    HAS_QT_SPELL = False

if HAS_QT_SPELL:
    class SpellHighlighter(QSyntaxHighlighter):
        """
        Real-time spell checking syntax highlighter.
        Adds red wavy underlines to misspelled words.
        """
        def __init__(self, document: QTextDocument):
            super().__init__(document)
            self.checker = get_shared_checker()

            # Format for misspelled words (antialiased red squiggly wave underline)
            self.error_format = QTextCharFormat()
            self.error_format.setFontUnderline(True)
            self.error_format.setUnderlineColor(QColor("#ff3333"))
            self.error_format.setUnderlineStyle(QTextCharFormat.UnderlineStyle.WaveUnderline)

        def highlightBlock(self, text: str):
            if not self.checker.is_ready or not text:
                return

            misspellings = self.checker.get_misspellings(text)
            for orig_word, sugg, pos in misspellings:
                self.setFormat(pos, len(orig_word), self.error_format)
