"""
Translate App - Невидимое приложение для перевода текста со скрина
"""

from .ocr_engine import OCREngine
from .translator import TextTranslator
from .screen_capture import ScreenCapture
from .voice_listener import VoiceListener

__all__ = ['OCREngine', 'TextTranslator', 'ScreenCapture', 'VoiceListener']
