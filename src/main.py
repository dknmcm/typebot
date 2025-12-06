import time
import threading
from datetime import datetime
from region_selector import RegionSelector
from screen_monitor import ScreenMonitor
from ocr_processor import OCRProcessor
from keystroke_generator import KeystrokeGenerator
from text_accumulator import TextAccumulator
from typing_manager import TypingManager
import os
from pathlib import Path
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.config import (
    SCREENSHOT_INTERVAL, MIN_OCR_CONFIDENCE,
    BASE_WPM, BASE_ERROR_RATE, SESSION_DURATION, SESSION_START_DELAY
)


class TypeBot:
    def __init__(self):
        self.monitor = ScreenMonitor()
        self.ocr = OCRProcessor()

        self.text_accumulator = TextAccumulator()
        self.typing_manager = TypingManager(self.text_accumulator)

        self.running = False
        self.monitor.screenshot_interval = SCREENSHOT_INTERVAL

    def start_session(self):
        """Main application entry point"""
        selector = RegionSelector(self.on_region_selected)
        selector.show_selector()

    def on_region_selected(self, x: int, y: int, width: int, height: int):
        self.monitor.set_region(x, y, width, height)
        self.monitor.register_change_callback(self.on_text_changed)
        self.start_monitoring_session()

    def start_monitoring_session(self):
        """Start 30-second continuous monitoring session"""
        time.sleep(SESSION_START_DELAY)

        self.running = True

        self.typing_manager.start()

        self.monitor.start_monitoring()

        session_thread = threading.Thread(target=self.run_session, daemon=True)
        session_thread.start()

        try:
            session_thread.join()
        except KeyboardInterrupt:
            self.stop_session()

    def run_session(self):
        start_time = time.time()

        while self.running and (time.time() - start_time) < SESSION_DURATION:
            remaining = SESSION_DURATION - (time.time() - start_time)
            if remaining > 0:
                time.sleep(1)

        self.stop_session()

    def on_text_changed(self, screenshot):
        """Process text changes and add to accumulator"""
        if not self.running:
            return

        try:
            # SAVE SCREENSHOTS
            # timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
            # os.makedirs("screenshots", exist_ok=True)
            # raw_path = f"screenshots/raw_{timestamp}.png"
            # screenshot.save(raw_path)
            # processed_image = self.ocr.preprocess_image(screenshot)
            # processed_path = f"screenshots/processed_{timestamp}.png"
            # processed_image.save(processed_path)

            text, confidence = self.ocr.get_text_with_confidence(screenshot)

            if confidence < MIN_OCR_CONFIDENCE or not text.strip():
                return

            new_words = self.text_accumulator.add_new_text(text)

        except Exception as e:
            print(f"Error processing text: {e}")

    def stop_session(self):
        """Stop both processes"""
        self.running = False

        self.typing_manager.stop()
        self.monitor.stop_monitoring()

    def get_session_stats(self):
        """Get current session statistics"""
        return {
            'running': self.running,
            'current_text_length': len(self.current_text),
            'last_processed_length': len(self.last_processed_text),
            'typing_stats': self.typist.session
        }


def main():
    """Main application entry point"""
    try:
        bot = TypeBot()
        bot.start_session()
    except Exception as e:
        print(f"Application error: {e}")


if __name__ == "__main__":
    main()
