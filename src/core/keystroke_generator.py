from pynput.keyboard import Key, Controller
import time
import random
from typing import Optional, Dict, List


class KeystrokeGenerator:
    def __init__(self):
        self.keyboard = Controller()
        self.typing_active = False

    def type_text(self, text: str, base_delay: float = 0.1):
        """Type text with basic timing"""
        self.typing_active = True

        try:
            for char in text:
                if not self.typing_active:
                    break

                self._type_character(char)

                # Basic delay between characters
                time.sleep(base_delay + random.uniform(-0.02, 0.02))

        except Exception as e:
            print(f"Error typing text: {e}")
        finally:
            self.typing_active = False

    def _type_character(self, char: str):
        """Type a single character with proper handling"""
        try:
            if char == ' ':
                # Space key
                self.keyboard.press(Key.space)
                time.sleep(0.05)  # Brief hold
                self.keyboard.release(Key.space)

            elif char == '\n':
                # Enter key
                self.keyboard.press(Key.enter)
                time.sleep(0.05)
                self.keyboard.release(Key.enter)

            elif char == '\t':
                # Tab key
                self.keyboard.press(Key.tab)
                time.sleep(0.05)
                self.keyboard.release(Key.tab)

            else:
                self.keyboard.press(char)
                time.sleep(0.05)
                self.keyboard.release(char)

        except Exception as e:
            print(f"Error typing character '{char}': {e}")

    def type_backspace(self, count: int = 1):
        """Type backspace key(s)"""
        for _ in range(count):
            self.keyboard.press(Key.backspace)
            time.sleep(0.05)
            self.keyboard.release(Key.backspace)
            time.sleep(0.1)  # Pause between backspaces

    def type_with_corrections(self, text: str, error_rate: float = 0.02):
        """Type text with occasional errors and corrections"""
        self.typing_active = True

        try:
            i = 0
            while i < len(text) and self.typing_active:
                char = text[i]

                # Randomly introduce errors
                if random.random() < error_rate and char.isalpha():
                    # Type wrong character first
                    wrong_char = random.choice('abcdefghijklmnopqrstuvwxyz')
                    self._type_character(wrong_char)
                    time.sleep(0.1)

                    # Realize mistake and backspace
                    time.sleep(0.3)  # Pause before correction
                    self.type_backspace(1)
                    time.sleep(0.1)

                # Type correct character
                self._type_character(char)

                # Variable delay between characters
                delay = random.uniform(0.08, 0.15)
                time.sleep(delay)

                i += 1

        except Exception as e:
            print(f"Error typing with corrections: {e}")
        finally:
            self.typing_active = False

    def stop_typing(self):
        """Stop current typing operation"""
        self.typing_active = False

    def test_typing(self):
        """Test basic typing functionality"""
        test_text = "Hello World! This is a test of the typing system."

        print("Starting typing test in 3 seconds...")
        print("Make sure cursor is in a text field!")

        for i in range(3, 0, -1):
            print(f"{i}...")
            time.sleep(1)

        print("Typing now...")
        self.type_text(test_text)
        print("Typing complete!")

    def test_typing_with_errors(self):
        """Test typing with error simulation"""
        test_text = "The quick brown fox jumps over the lazy dog."

        print("Starting error test in 3 seconds...")
        print("Make sure cursor is in a text field!")

        for i in range(3, 0, -1):
            print(f"{i}...")
            time.sleep(1)

        print("Typing with errors...")
        self.type_with_corrections(test_text, error_rate=0.1)
        print("Typing complete!")
