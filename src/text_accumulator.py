import threading
import difflib
from typing import List, Set


class TextAccumulator:
    def __init__(self):
        self.master_text = ""
        self.master_words = []
        self.seen_words = set()
        self.lock = threading.Lock()

    def add_new_text(self, ocr_text: str) -> str:
        """Add new text to master string, return only new words added"""
        if not ocr_text.strip():
            return ""

        with self.lock:
            # Normalize and split into words
            new_words = ocr_text.strip().split()

            if not self.master_words:
                # First text - add everything
                self.master_words = new_words.copy()
                self.seen_words = set(enumerate(new_words))
                self.master_text = ' '.join(self.master_words)
                print(f"Initial text: '{self.master_text}'")
                return self.master_text

            # Find new words using sequence matching
            new_additions = self._find_new_words(new_words)

            if new_additions:
                self.master_words.extend(new_additions)
                self.master_text = ' '.join(self.master_words)
                new_text = ' '.join(new_additions)
                print(f"Master text now: '{self.master_text}'")
                return new_text

            return ""

    def _find_new_words(self, new_words: List[str]) -> List[str]:
        """Find words that haven't been seen before"""
        # Use sequence matcher to find overlap
        matcher = difflib.SequenceMatcher(None, self.master_words, new_words)

        for i in range(1, min(len(self.master_words), len(new_words)) + 1):
            master_suffix = self.master_words[-i:]
            new_prefix = new_words[:i]

            if [w.lower() for w in master_suffix] == [w.lower() for w in new_prefix]:
                # Found overlap, return everything after
                new_additions = new_words[i:]
                print(f"Found suffix/prefix match (overlap: {i}), adding: {new_additions}")
                return new_additions

    def get_master_text(self) -> str:
        """Get current master text"""
        with self.lock:
            return self.master_text

    def get_word_count(self) -> int:
        """Get total word count"""
        with self.lock:
            return len(self.master_words)

    def reset(self):
        """Reset accumulator"""
        with self.lock:
            self.master_text = ""
            self.master_words = []
            self.seen_words = set()
