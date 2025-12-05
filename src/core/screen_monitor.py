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

    def set_region(self, x: int, y: int, width: int, height: int):
        """Set the screen region to monitor"""

    def register_change_callback(self, callback: Callable):
        """Register function to call when changes detected"""

    def start_monitoring(self):
        """Begin background screenshot monitoring"""

    def stop_monitoring(self):
        """Stop monitoring and cleanup thread"""

    def _monitor_loop(self):
        """Main monitoring loop (runs in separate thread)"""

    def _capture_region(self) -> Image:
        """Capture screenshot of specified region"""

    def _get_image_hash(self, image: Image) -> str:
        """Generate hash for change detection"""
