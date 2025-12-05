import os
import time
from datetime import datetime
from src.core.region_selector import RegionSelector
from src.core.screen_monitor import ScreenMonitor
from src.core.ocr_processor import OCRProcessor
from src.core.keystroke_generator import KeystrokeGenerator


def test_full_typing_pipeline():
    """Test complete pipeline: Region → Screenshot → OCR → Typing"""

    os.makedirs("screenshots", exist_ok=True)

    monitor = ScreenMonitor()
    ocr = OCRProcessor()
    typist = KeystrokeGenerator()

    def on_region_selected(x, y, width, height):
        """Called when user confirms region selection"""
        print(f"Region selected: x={x}, y={y}, width={width}, height={height}")

        monitor.set_region(x, y, width, height)

        print("Taking screenshot...")
        screenshot = monitor._capture_region()

        if screenshot:
            # Save screenshot for reference
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot.save(f"screenshots/pipeline_{timestamp}.png")

            # Extract text via OCR
            print("Extracting text...")
            text, confidence = ocr.get_text_with_confidence(screenshot)

            print("\n--- Pipeline Results ---")
            print(f"Extracted text: '{text}'")
            print(f"OCR confidence: {confidence:.1f}%")

            if confidence < 70:
                print("Low confidence - typing may have errors")

            if text.strip():
                print(f"\nReady to type {len(text)} characters...")
                print("Click in a text field where you want the text typed.")

                for i in range(5, 0, -1):
                    print(f"Starting in {i}...")
                    time.sleep(1)

                typist.type_text(text, base_delay=0.1)
            else:
                print("No text extracted - try selecting a clearer text region")
        else:
            print("Failed to capture screenshot")

    print("Full Pipeline Test")
    print("1. Position window over text you want to copy")
    print("2. Click 'Start' to capture")
    print("3. Switch to target text field")
    print("4. Bot will type the captured text")

    selector = RegionSelector(on_region_selected)
    selector.show_selector()


if __name__ == "__main__":
    test_full_typing_pipeline()
