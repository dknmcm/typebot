from pynput.keyboard import Key, Controller
import time
import random
from typing import Optional, Dict, List, Tuple
from dataclasses import dataclass
import os
from pathlib import Path
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.config import BASE_WPM, BASE_ERROR_RATE, CHAR_PAIR_ADJUSTMENTS, COMMON_TYPOS


@dataclass
class TypingSession:
    start_time: float
    characters_typed: int = 0
    errors_made: int = 0
    base_wpm: float = 60.0
    current_fatigue: float = 0.0


class KeystrokeGenerator:
    def __init__(self, base_wpm: float = BASE_WPM, error_rate: float = BASE_ERROR_RATE):
        self.keyboard = Controller()
        self.typing_active = False
        self.base_wpm = base_wpm
        self.error_rate = error_rate
        self.session = TypingSession(start_time=time.time(), base_wpm=base_wpm)

        self.char_pair_delays = CHAR_PAIR_ADJUSTMENTS
        self.common_typos = COMMON_TYPOS

    def type_human_like(self, text: str):
        """Type text with realistic human behavior"""
        self.typing_active = True
        self.session = TypingSession(start_time=time.time(), base_wpm=self.base_wpm)

        try:
            previous_char = None

            for i, char in enumerate(text):
                if not self.typing_active:
                    break

                should_error, actual_char = self._should_make_error(char)

                delay = self._get_keystroke_delay(char, previous_char)
                time.sleep(delay)

                if should_error:
                    self._type_character(actual_char)
                    self.session.errors_made += 1

                    correction_delay = self._get_correction_delay()
                    time.sleep(correction_delay)

                    self.type_backspace(1)
                    time.sleep(0.1)

                self._type_character(char)
                self.session.characters_typed += 1

                if i % 20 == 0:
                    self._update_fatigue()

                if char == ' ':
                    time.sleep(self._get_word_pause_delay())
                elif char in '.!?':
                    time.sleep(self._get_sentence_pause_delay())

                previous_char = char

        except Exception as e:
            print(f"Error in human-like typing: {e}")
        finally:
            self.typing_active = False

    def _get_keystroke_delay(self, current_char: str, previous_char: str = None) -> float:
        """Calculate realistic delay before typing character"""
        chars_per_second = (self.base_wpm * 5) / 60
        base_delay = 1.0 / chars_per_second

        variation = random.uniform(-0.2, 0.2)
        delay = base_delay * (1 + variation)

        if previous_char and current_char:
            pair = previous_char.lower() + current_char.lower()
            if pair in self.char_pair_delays:
                delay += self.char_pair_delays[pair]

        fatigue_factor = 1 + (self.session.current_fatigue * 0.3)
        delay *= fatigue_factor

        if random.random() < 0.05:
            delay += random.uniform(0.3, 1.0)

        return max(delay, 0.05)

    def _should_make_error(self, char: str) -> Tuple[bool, str]:
        """Determine if error should be made and what typo"""
        if not char.isalpha():
            return False, char

        error_probability = self.error_rate + (self.session.current_fatigue * 0.02)

        if random.random() < error_probability:
            char_lower = char.lower()
            if char_lower in self.common_typos:
                typo = random.choice(self.common_typos[char_lower])
                typo = typo.upper() if char.isupper() else typo
                return True, typo

        return False, char

    def _get_correction_delay(self) -> float:
        """Get delay before correcting mistake"""
        return random.uniform(0.2, 0.8) if random.random() < 0.3 else random.uniform(0.5, 1.5)

    def _get_word_pause_delay(self) -> float:
        """Get delay between words"""
        return random.uniform(0.1, 0.3)

    def _get_sentence_pause_delay(self) -> float:
        """Get delay after sentences"""
        return random.uniform(0.5, 1.2)

    def _update_fatigue(self):
        """Update typing fatigue"""
        self.session.current_fatigue = min(0.5, self.session.characters_typed / 500.0)

        # Occasional energy boost
        if self.session.characters_typed > 100 and random.random() < 0.1:
            self.session.current_fatigue *= 0.7
