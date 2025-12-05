import time
import threading
from datetime import datetime
from region_selector import RegionSelector
from screen_monitor import ScreenMonitor
from ocr_processor import OCRProcessor
from keystroke_generator import KeystrokeGenerator
import os
from pathlib import Path
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.config import (
    SCREENSHOT_INTERVAL, MIN_OCR_CONFIDENCE,
    BASE_WPM, BASE_ERROR_RATE
)


class TypeBot:
    def __init__(self):
        self.monitor = ScreenMonitor()
        self.ocr = OCRProcessor()
        self.typist = KeystrokeGenerator(BASE_WPM, BASE_ERROR_RATE)

        self.running = False
        self.current_text = ""
        self.last_processed_text = ""

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
        self.running = True

        self.monitor.start_monitoring()

        session_thread = threading.Thread(target=self.run_session, daemon=True)
        session_thread.start()

        try:
            session_thread.join()
        except KeyboardInterrupt:
            self.stop_session()

    def run_session(self):
        """Run monitoring session for 30 seconds"""
        start_time = time.time()
        session_duration = 30.0

        while self.running and (time.time() - start_time) < session_duration:
            remaining = session_duration - (time.time() - start_time)
            if remaining > 0:
                time.sleep(1)

        self.stop_session()

    def on_text_changed(self, screenshot):
        """Called when screen content changes"""
        if not self.running:
            return

        try:
            text, confidence = self.ocr.get_text_with_confidence(screenshot)

            if confidence < MIN_OCR_CONFIDENCE:
                print(f"Low OCR confidence ({confidence:.1f}%) - skipping")
                return

            if not text.strip():
                return

            if self.ocr.is_text_similar(text, self.last_processed_text):
                return

            self.process_new_text(text, confidence)

        except Exception as e:
            print(f"Error processing text change: {e}")

    def process_new_text(self, text: str, confidence: float):
        """Process and type new text"""
        new_content = self.get_text_difference(self.last_processed_text, text)

        if new_content.strip():
            timestamp = datetime.now().strftime("%H:%M:%S")
            print(f"\n[{timestamp}] 📝 New text detected (confidence: {confidence:.1f}%)")
            print(f"Typing: '{new_content}'")

            typing_thread = threading.Thread(
                target=self.typist.type_human_like,
                args=(new_content,),
                daemon=True
            )
            typing_thread.start()

            self.last_processed_text = text

    def get_text_difference(self, old_text: str, new_text: str) -> str:
        """Extract new content from text comparison"""
        if len(new_text) > len(old_text) and old_text in new_text:
            old_end = new_text.find(old_text) + len(old_text)
            return new_text[old_end:].strip()

        if old_text != new_text:
            return new_text.strip()

        return ""

    def stop_session(self):
        """Stop monitoring session"""
        print("\nStopping session...")
        self.running = False

        # Stop components
        if self.monitor:
            self.monitor.stop_monitoring()

        if self.typist:
            self.typist.stop_typing()

        print("✅ Session stopped")

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
