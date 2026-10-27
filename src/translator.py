from googletrans import Translator, LANGUAGES
import re

class TextTranslator:
    def __init__(self):
        self.translator = Translator()

    def translate_to_russian(self, text, source_lang='auto'):
        """
        Переводит текст на русский язык
        text: текст для перевода
        source_lang: язык источника (auto для автоматического определения)
        Возвращает: переведённый текст
        """
        try:
            if not text or text.strip() == '':
                return ''

            result = self.translator.translate(text, src_language=source_lang, dest_language='ru')
            return result['text']
        except Exception as e:
            print(f"Ошибка перевода: {e}")
            return text

    def translate_text_with_positions(self, text_data):
        """
        Переводит текст сохраняя позиции и bounding boxes
        text_data: список словарей {'text': '...', 'bbox': [...], 'confidence': 0.9}
        Возвращает: список с переведённым текстом и исходными координатами
        """
        translated_data = []
        for item in text_data:
            original_text = item['text']
            translated_text = self.translate_to_russian(original_text)

            translated_data.append({
                'original': original_text,
                'translated': translated_text,
                'bbox': item['bbox'],
                'confidence': item['confidence']
            })

        return translated_data

    def detect_language(self, text):
        """Определяет язык текста"""
        try:
            detection = self.translator.detect(text)
            return detection['language']
        except:
            return 'unknown'
