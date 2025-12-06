from pynput.keyboard import Key, Controller
import time
import random
from typing import Optional, Dict, List, Tuple
from dataclasses import dataclass
import os
from pathlib import Path
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.config import (
    BASE_WPM, BASE_ERROR_RATE, UNCORRECTED_ERROR_RATE, CHAR_PAIR_ADJUSTMENTS, COMMON_TYPOS,
    WPM_VARIATION, MIN_KEYSTROKE_DELAY, MAX_THINKING_PAUSE,
    WORD_PAUSE_MIN, WORD_PAUSE_MAX, SENTENCE_PAUSE_MIN, SENTENCE_PAUSE_MAX,
    CORRECTION_DELAY_MIN, CORRECTION_DELAY_MAX, MAX_FATIGUE, FATIGUE_BUILDUP_CHARS,
    ENERGY_BOOST_CHANCE, FATIGUE_ERROR_MULTIPLIER, THINKING_PAUSE_PROBABILITY
)


@dataclass
class TypingSession:
    start_time: float
    characters_typed: int = 0
    errors_made: int = 0
    base_wpm: float = BASE_WPM
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

    def _get_keystroke_delay(self, current_char: str, previous_char: str = None) -> float:
        """Calculate realistic delay before typing character"""
        chars_per_second = (self.base_wpm * 5) / 60
        base_delay = 1.0 / chars_per_second

        variation = random.uniform(-WPM_VARIATION, WPM_VARIATION)
        delay = base_delay * (1 + variation)

        if previous_char and current_char:
            pair = previous_char.lower() + current_char.lower()
            if pair in self.char_pair_delays:
                delay += self.char_pair_delays[pair]

        fatigue_factor = 1 + (self.session.current_fatigue * 0.3)
        delay *= fatigue_factor

        if random.random() < THINKING_PAUSE_PROBABILITY:
            delay += random.uniform(0.0, MAX_THINKING_PAUSE)

        return max(delay, 0.05)

    def _should_make_error(self, char: str) -> Tuple[bool, str]:
        """Determine if error should be made and what typo"""
        if not char.isalpha():
            return False, char

        error_probability = self.error_rate + (self.session.current_fatigue * FATIGUE_ERROR_MULTIPLIER)

        if random.random() < error_probability:
            char_lower = char.lower()
            if char_lower in self.common_typos:
                typo = random.choice(self.common_typos[char_lower])
                typo = typo.upper() if char.isupper() else typo
                return True, typo

        return False, char
    
    def _should_make_uncorrected_error(self, char: str) -> Tuple[bool, str]:
        """Determine if an uncorrected error should be made"""
        if not char.isalpha():
            return False, char

        error_probability = UNCORRECTED_ERROR_RATE + (self.session.current_fatigue * FATIGUE_ERROR_MULTIPLIER)

        if random.random() < error_probability:
            char_lower = char.lower()
            if char_lower in self.common_typos:
                typo = random.choice(self.common_typos[char_lower])
                typo = typo.upper() if char.isupper() else typo
                return True, typo

        return False, char

    def _get_correction_delay(self) -> float:
        """Get delay before correcting mistake"""
        return random.uniform(CORRECTION_DELAY_MIN, CORRECTION_DELAY_MAX)

    def _get_word_pause_delay(self) -> float:
        """Get delay between words"""
        return random.uniform(WORD_PAUSE_MIN, WORD_PAUSE_MAX)

    def _get_sentence_pause_delay(self) -> float:
        """Get delay after sentences"""
        return random.uniform(SENTENCE_PAUSE_MIN, SENTENCE_PAUSE_MAX)

    def _update_fatigue(self):
        """Update typing fatigue"""
        self.session.current_fatigue = min(MAX_FATIGUE, 
                                           self.session.characters_typed / 
                                           FATIGUE_BUILDUP_CHARS)

        # Occasional energy boost
        if self.session.characters_typed > 100 and random.random() < ENERGY_BOOST_CHANCE: 
            self.session.current_fatigue *= 0.7

    def _type_character(self, char: str):
        """Type a single character"""
        try:
            if char == '\n':
                self.keyboard.press(Key.enter)
                time.sleep(0.03)
                self.keyboard.release(Key.enter)
            elif char == '\t':
                self.keyboard.press(Key.tab)
                time.sleep(0.03)
                self.keyboard.release(Key.tab)
            else:
                self.keyboard.type(char)
                time.sleep(0.0)
        except Exception as e:
            print(f"Error typing character '{char}': {e}")

    def type_backspace(self, count: int = 1):
        """Type backspace key(s)"""
        for _ in range(count):
            self.keyboard.press(Key.backspace)
            time.sleep(0.05)
            self.keyboard.release(Key.backspace)
            time.sleep(0.1)

    def stop_typing(self):
        """Stop current typing operation"""
        self.typing_active = False
