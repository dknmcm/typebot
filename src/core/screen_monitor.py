import mss
import hashlib
import time
import threading
from typing import Callable, Optional, Tuple, Dict
import numpy as np
from PIL import Image


class ScreenMonitor:
    def __init__(self):
        self.region = None
        self.monitoring = False
        self.monitor_thread = None
        self.change_callback = None
        self.last_hash = None
        self.screenshot_interval = 0.5
        self.sct = mss.mss()

    def set_region(self, x: int, y: int, width: int, height: int):
        """Set the screen region to monitor"""
        self.region = {"top": y, "left": x, "width": width, "height": height}
        print(f"Screen region set: {x},{y} ({width}x{height})")

    def register_change_callback(self, callback: Callable[[Image.Image], None]):
        """Register function to call when changes detected"""
        self.change_callback = callback

    def start_monitoring(self):
        """Begin background screenshot monitoring"""
        if not self.region:
            raise ValueError("No region set. Call set_region() first.")

        if self.monitoring:
            print("Already monitoring")
            return

        self.monitoring = True
        self.last_hash = None

        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()
        print("Screen monitoring started")

    def stop_monitoring(self):
        """Stop monitoring and cleanup thread"""
        if not self.monitoring:
            return

        self.monitoring = False

        # Wait for thread to finish
        if self.monitor_thread and self.monitor_thread.is_alive():
            self.monitor_thread.join(timeout=1.0)

        print("Screen monitoring stopped")

    def _monitor_loop(self):
        print("Monitor loop started")

        while self.monitoring:
            try:
                screenshot = self._capture_region()

                if screenshot:
                    current_hash = self._get_image_hash(screenshot)

                    # Check if image changed
                    if current_hash != self.last_hash:
                        print(f"Change detected! Hash: {current_hash[:8]}...")
                        self.last_hash = current_hash

                        if self.change_callback:
                            self.change_callback(screenshot)
                        else:
                            print("No callback registered for change detection")

                # Wait before next capture
                time.sleep(self.screenshot_interval)

            except Exception as e:
                print(f"Error in monitor loop: {e}")
                time.sleep(self.screenshot_interval)

        print("Monitor loop ended")

    def _capture_region(self) -> Optional[Image.Image]:
        try:
            screenshot = self.sct.grab(self.region)
            image = Image.frombytes('RGB', screenshot.size, screenshot.rgb)

            return image

        except Exception as e:
            print(f"Error capturing screenshot: {e}")
            return None

    def _get_image_hash(self, image: Image.Image) -> str:
        try:
            small_image = image.resize((16, 16), Image.Resampling.LANCZOS)

            # Convert to grayscale to ignore minor color variations
            gray_image = small_image.convert('L')

            # Apply slight blur to reduce noise from anti-aliasing
            from PIL import ImageFilter
            blurred = gray_image.filter(ImageFilter.BLUR)

            image_bytes = blurred.tobytes()
            hash_obj = hashlib.md5(image_bytes)

            return hash_obj.hexdigest()

        except Exception as e:
            print(f"Error generating image hash: {e}")
            return str(time.time())

    def get_status(self) -> Dict[str, any]:
        return {
            "monitoring": self.monitoring,
            "region_set": self.region is not None,
            "last_hash": self.last_hash[:8] + "..." if self.last_hash else None,
            "interval": self.screenshot_interval
        }
