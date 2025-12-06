import threading
import time
from keystroke_generator import KeystrokeGenerator
from text_accumulator import TextAccumulator
from config.config import BASE_WPM, BASE_ERROR_RATE


class TypingManager:
    def __init__(self, text_accumulator: TextAccumulator):
        self.typist = KeystrokeGenerator(BASE_WPM, BASE_ERROR_RATE)
        self.text_accumulator = text_accumulator
        self.typing_index = 0
        self.typing_thread = None
        self.running = False

    def start(self):
        """Start independent typing process"""
        self.running = True
        self.typing_thread = threading.Thread(target=self._typing_worker, daemon=True)
        self.typing_thread.start()

    def _typing_worker(self):
        """Independent typing worker that follows master text"""
        while self.running:
            try:
                master_text = self.text_accumulator.get_master_text()

                if len(master_text) > self.typing_index:
                    remaining_text = master_text[self.typing_index:]

                    previous_char = None
                    for i, char in enumerate(remaining_text):
                        if not self.running:
                            break

                        should_error, actual_char = self.typist._should_make_error(char)

                        delay = self.typist._get_keystroke_delay(char, previous_char)
                        time.sleep(delay)

                        if should_error:
                            self.typist._type_character(actual_char)
                            self.typist.session.errors_made += 1

                            correction_delay = self.typist._get_correction_delay()
                            time.sleep(correction_delay)

                            self.typist.type_backspace(1)
                            time.sleep(0.02)

                            self.typist._type_character(char)
                        else:
                            # Check for uncorrected errors
                            should_uncorrected_error, uncorrected_char = self.typist._should_make_uncorrected_error(char)

                            if should_uncorrected_error:
                                self.typist._type_character(uncorrected_char)
                                self.typist.session.errors_made += 1
                            else:
                                self.typist._type_character(char)

                        self.typing_index += 1
                        self.typist.session.characters_typed += 1

                        # if i % 100 == 0:
                        #     self.typist._update_fatigue()

                        if char == ' ':
                            time.sleep(self.typist._get_word_pause_delay())
                        elif char in '.!?':
                            time.sleep(self.typist._get_sentence_pause_delay())

                        previous_char = char
                else:
                    time.sleep(0.01)

            except Exception as e:
                time.sleep(0.05)

    def stop(self):
        """Stop typing process"""
        self.running = False
        self.typist.stop_typing()

        if self.typing_thread and self.typing_thread.is_alive():
            self.typing_thread.join(timeout=2.0)

    def get_typing_progress(self):
        master_text = self.text_accumulator.get_master_text()
        return {
            'typed_chars': self.typing_index,
            'total_chars': len(master_text),
            'remaining': len(master_text) - self.typing_index,
            'progress_percent': (self.typing_index / len(master_text) * 100) if master_text else 0
        }

    def reset_index(self):
        """Reset typing index to start over"""
        self.typing_index = 0
