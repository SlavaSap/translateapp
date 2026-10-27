import easyocr
import numpy as np
from PIL import Image
import io

class OCREngine:
    def __init__(self):
        self.reader = easyocr.Reader(['ru', 'en', 'uk', 'de', 'fr', 'es', 'ja', 'zh'])

    def extract_text_from_image(self, image_data):
        """
        Извлекает текст из изображения
        image_data: numpy array или PIL Image
        Возвращает: список (text, coordinates, confidence)
        """
        try:
            if isinstance(image_data, np.ndarray):
                image = image_data
            else:
                image = np.array(image_data)

            results = self.reader.readtext(image, detail=1)

            text_data = []
            for (bbox, text, confidence) in results:
                text_data.append({
                    'text': text,
                    'bbox': bbox,
                    'confidence': confidence
                })

            return text_data
        except Exception as e:
            print(f"Ошибка OCR: {e}")
            return []

    def get_full_text(self, image_data):
        """Получить весь текст из изображения как строку"""
        text_data = self.extract_text_from_image(image_data)
        return ' '.join([item['text'] for item in text_data])
