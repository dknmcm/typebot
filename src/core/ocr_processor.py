import pytesseract
import cv2
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
from typing import Optional, Tuple, Dict
import re


class OCRProcessor:
    def __init__(self):
        # Configure Tesseract for best text recognition
        self.tesseract_config = '--oem 3 --psm 6 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789.,!?;:\'"()[]{}+-=/<>@#$%^&*_|\\~` '

        # Basic config without character restrictions (for general text)
        self.basic_config = '--oem 3 --psm 6'

    def extract_text(self, image: Image.Image) -> str:
        """Extract text from image using OCR"""
        try:
            # Preprocess image for better OCR
            processed_image = self.preprocess_image(image)

            # Extract text using Tesseract
            text = pytesseract.image_to_string(processed_image, config=self.basic_config)

            # Clean up the extracted text
            cleaned_text = self._clean_text(text)

            return cleaned_text

        except Exception as e:
            print(f"Error extracting text: {e}")
            return ""

    def preprocess_image(self, image: Image.Image) -> Image.Image:
        """Optimize image for OCR accuracy"""
        try:
            # Convert to RGB if needed
            if image.mode != 'RGB':
                image = image.convert('RGB')

            # Scale up image for better OCR (3x larger)
            width, height = image.size
            image = image.resize((width * 3, height * 3), Image.Resampling.LANCZOS)

            # Convert to grayscale
            gray_image = image.convert('L')

            # Enhance contrast
            enhancer = ImageEnhance.Contrast(gray_image)
            contrast_image = enhancer.enhance(2.0)  # Increase contrast

            # Convert to numpy array for OpenCV processing
            img_array = np.array(contrast_image)

            # Apply Gaussian blur to reduce noise
            blurred = cv2.GaussianBlur(img_array, (1, 1), 0)

            # Apply threshold to get binary image
            _, binary = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

            # Convert back to PIL Image
            processed_image = Image.fromarray(binary)

            return processed_image

        except Exception as e:
            print(f"Error preprocessing image: {e}")
            return image  # Return original if processing fails

    def get_text_with_confidence(self, image: Image.Image) -> Tuple[str, float]:
        """Extract text and return confidence score"""
        try:
            processed_image = self.preprocess_image(image)

            data = pytesseract.image_to_data(processed_image, config=self.basic_config, output_type=pytesseract.Output.DICT)

            words = []
            confidences = []

            for i, confidence in enumerate(data['conf']):
                if confidence > 0:
                    text = data['text'][i].strip()
                    if text:
                        words.append(text)
                        confidences.append(confidence)

            full_text = ' '.join(words)
            avg_confidence = sum(confidences) / len(confidences) if confidences else 0

            cleaned_text = self._clean_text(full_text)

            return cleaned_text, avg_confidence

        except Exception as e:
            print(f"Error extracting text with confidence: {e}")
            return "", 0.0

    def _clean_text(self, text: str) -> str:
        """Clean up extracted text"""
        if not text:
            return ""

        # Remove extra whitespace and newlines
        cleaned = re.sub(r'\s+', ' ', text.strip())

        # Remove common OCR artifacts
        cleaned = cleaned.replace('|', 'l')
        cleaned = cleaned.replace('0', 'O')

        return cleaned

    def is_text_similar(self, text1: str, text2: str, threshold: float = 0.8) -> bool:
        """Check if two texts are similar (for change detection)"""
        if not text1 and not text2:
            return True
        if not text1 or not text2:
            return False

        text1_clean = text1.lower().replace(' ', '')
        text2_clean = text2.lower().replace(' ', '')

        if len(text1_clean) == 0 and len(text2_clean) == 0:
            return True

        longer_text = max(text1_clean, text2_clean, key=len)
        shorter_text = min(text1_clean, text2_clean, key=len)

        if len(longer_text) == 0:
            return True

        matches = sum(1 for a, b in zip(longer_text, shorter_text) if a == b)
        similarity = matches / len(longer_text)

        return similarity >= threshold

    def debug_save_processed_image(self, image: Image.Image, filename: str):
        """Save processed image for debugging OCR issues"""
        try:
            processed = self.preprocess_image(image)
            processed.save(filename)
            print(f"Processed image saved: {filename}")
        except Exception as e:
            print(f"Error saving processed image: {e}")
