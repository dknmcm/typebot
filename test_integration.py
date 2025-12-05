import os
import time
from datetime import datetime
from src.core.region_selector import RegionSelector
from src.core.screen_monitor import ScreenMonitor
from src.core.ocr_processor import OCRProcessor


def test_single_ocr():
    """Test single screenshot + OCR extraction"""
    os.makedirs("screenshots", exist_ok=True)

    monitor = ScreenMonitor()
    ocr = OCRProcessor()

    def on_region_selected(x, y, width, height):
        """Called when user confirms region selection"""
        print(f"Region selected: x={x}, y={y}, width={width}, height={height}")

        # Set region and take one screenshot
        monitor.set_region(x, y, width, height)

        print("Taking screenshot...")
        screenshot = monitor._capture_region()

        if screenshot:
            # Save original screenshot
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            original_file = f"screenshots/original_{timestamp}.png"
            screenshot.save(original_file)
            print(f"Original saved: {original_file}")

            # Save processed image for comparison
            processed_file = f"screenshots/processed_{timestamp}.png"
            ocr.debug_save_processed_image(screenshot, processed_file)

            # Extract text with confidence
            text, confidence = ocr.get_text_with_confidence(screenshot)

            print("\n--- OCR Results ---")
            print(f"Extracted text: '{text}'")
            print(f"Confidence: {confidence:.1f}%")
            print(f"Text length: {len(text)} characters")

            if confidence < 50:
                print("⚠️  Low confidence - try selecting clearer text")
            elif confidence < 80:
                print("⚠️  Medium confidence - results may have errors")
            else:
                print("✅ High confidence - results should be accurate")

        else:
            print("Failed to capture screenshot")

    print("Single OCR Test")
    print("1. Position window over clear text")
    print("2. Click 'Start' to capture and analyze")

    selector = RegionSelector(on_region_selected)
    selector.show_selector()


if __name__ == "__main__":
    test_single_ocr()
