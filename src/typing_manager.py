import threading
import time
from queue import Queue
from keystroke_generator import KeystrokeGenerator
from config.config import BASE_WPM, BASE_ERROR_RATE


class TypingManager:
    def __init__(self):
        self.typist = KeystrokeGenerator(BASE_WPM, BASE_ERROR_RATE)
        self.typing_queue = Queue()
        self.typing_thread = None
        self.running = False

    def start(self):
        """Start independent typing process"""
        self.running = True
        self.typing_thread = threading.Thread(target=self._typing_worker, daemon=True)
        self.typing_thread.start()

    def add_text_to_type(self, text: str):
        """Add text to typing queue"""
        if text.strip():
            self.typing_queue.put(text.strip())

    def _typing_worker(self):
        """Independent typing worker thread"""
        while self.running:
            try:
                # Wait for text to type (with timeout)
                text = self.typing_queue.get(timeout=1.0)

                if text and self.running:
                    self.typist.type_human_like(text)

                self.typing_queue.task_done()

            except:
                # Timeout or other error - continue loop
                continue

    def stop(self):
        """Stop typing process"""
        self.running = False
        self.typist.stop_typing()

        if self.typing_thread and self.typing_thread.is_alive():
            self.typing_thread.join(timeout=2.0)

    def clear_queue(self):
        """Clear pending typing tasks"""
        while not self.typing_queue.empty():
            try:
                self.typing_queue.get_nowait()
                self.typing_queue.task_done()
            except:
                break
