import os
import time
from datetime import datetime
from src.core.region_selector import RegionSelector
from src.core.screen_monitor import ScreenMonitor


def test_region_and_screenshot():
    """Test region selection + single screenshot capture"""

    # Create screenshots directory if it doesn't exist
    os.makedirs("screenshots", exist_ok=True)

    monitor = ScreenMonitor()

    def on_region_selected(x, y, width, height):
        """Called when user confirms region selection"""
        print(f"Region selected: x={x}, y={y}, width={width}, height={height}")

        # Set region in monitor
        monitor.set_region(x, y, width, height)

        # Take single screenshot
        print("Capturing screenshot...")
        screenshot = monitor._capture_region()

        if screenshot:
            # Save screenshot with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"screenshots/test_capture_{timestamp}.png"
            screenshot.save(filename)
            print(f"Screenshot saved: {filename}")
            print(f"Image size: {screenshot.size}")
        else:
            print("Failed to capture screenshot")

    # Start region selection
    print("Starting region selector...")
    print("1. Position and resize the window over text you want to capture")
    print("2. Click 'Start' button")
    print("3. Check screenshots/ folder for the captured image")

    selector = RegionSelector(on_region_selected)
    selector.show_selector()


if __name__ == "__main__":
    test_region_and_screenshot()
