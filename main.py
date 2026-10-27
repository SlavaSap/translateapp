from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle

from src.ocr_engine import OCREngine
from src.translator import TextTranslator
from src.screen_capture import ScreenCapture
from src.voice_listener import VoiceListener

import threading
import os
from PIL import Image as PILImage
from PIL import ImageDraw, ImageFont
import numpy as np

class TranslateOverlay:
    """Класс для отображения переведённого текста поверх оригинала"""

    def __init__(self, translated_data, original_image):
        self.translated_data = translated_data
        self.original_image = original_image.copy()
        self.overlay_image = self._create_overlay()

    def _create_overlay(self):
        """Создаёт изображение с переведённым текстом"""
        overlay = self.original_image.copy()
        draw = ImageDraw.Draw(overlay)

        # Пытаемся загрузить шрифт
        try:
            font = ImageFont.truetype("arial.ttf", 20)
        except:
            font = ImageFont.load_default()

        # Рисуем переведённый текст поверх оригинала
        for item in self.translated_data:
            bbox = item['bbox']
            translated_text = item['translated']

            # Получаем координаты (первая и третья точки bbox)
            if len(bbox) >= 2:
                x = int(bbox[0][0])
                y = int(bbox[0][1])

                # Рисуем полупрозрачный фон
                draw.rectangle([x, y, x + 200, y + 40], fill=(255, 255, 255, 200))

                # Пишем переведённый текст
                draw.text((x + 5, y + 5), translated_text, fill=(0, 0, 0), font=font)

        return overlay

    def get_image(self):
        return self.overlay_image

class TranslateApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.ocr_engine = OCREngine()
        self.translator = TextTranslator()
        self.screen_capture = ScreenCapture()
        self.voice_listener = VoiceListener(callback=self.on_voice_command)

        self.is_translating = False
        self.current_image = None
        self.current_translated_image = None

    def build(self):
        """Строит UI приложения"""
        Window.size = (400, 600)

        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Заголовок
        title = Label(text='Translate App', size_hint_y=0.1, bold=True, font_size='20sp')
        main_layout.add_widget(title)

        # Основная область для изображения
        self.image_display = Image(size_hint_y=0.6)
        main_layout.add_widget(self.image_display)

        # Кнопки управления
        button_layout = GridLayout(cols=2, size_hint_y=0.2, spacing=10)

        start_btn = Button(text='Начать слушание')
        start_btn.bind(on_press=self.start_listening)
        button_layout.add_widget(start_btn)

        stop_btn = Button(text='Остановить')
        stop_btn.bind(on_press=self.stop_listening)
        button_layout.add_widget(stop_btn)

        capture_btn = Button(text='Скриншот')
        capture_btn.bind(on_press=self.capture_screenshot)
        button_layout.add_widget(capture_btn)

        translate_btn = Button(text='Перевести')
        translate_btn.bind(on_press=self.translate_screenshot)
        button_layout.add_widget(translate_btn)

        main_layout.add_widget(button_layout)

        # Статус-бар
        self.status_label = Label(text='Готов', size_hint_y=0.1)
        main_layout.add_widget(self.status_label)

        # Автозапуск слушания
        Clock.schedule_once(lambda dt: self.start_listening_auto(), 1)

        return main_layout

    def start_listening_auto(self):
        """Автоматически начинает слушать при запуске"""
        self.start_listening()
        self.status_label.text = "Слушаю команду 'ТРАНСЛЕЙТ'..."

    def start_listening(self, instance=None):
        """Начинает слушать голосовые команды"""
        if not self.voice_listener.listening:
            self.voice_listener.start_listening()
            self.status_label.text = "Слушаю команду..."

    def stop_listening(self, instance=None):
        """Останавливает слушание"""
        self.voice_listener.stop_listening()
        self.status_label.text = "Слушание остановлено"

    def on_voice_command(self, command):
        """Обработчик голосовой команды"""
        print(f"Команда получена: {command}")
        self.status_label.text = f"Команда: {command}"

        # Автоматически делаем скриншот и переводим
        Clock.schedule_once(lambda dt: self.capture_screenshot(), 0.5)
        Clock.schedule_once(lambda dt: self.translate_screenshot(), 1.5)

    def capture_screenshot(self, instance=None):
        """Захватывает скриншот"""
        self.status_label.text = "Захватываю скриншот..."

        # Делаем это в отдельном потоке
        def capture_thread():
            try:
                # Пытаемся использовать ADB (если подключено устройство)
                import subprocess
                result = subprocess.run(
                    ["adb", "shell", "screencap", "-p", "/sdcard/translate.png"],
                    capture_output=True,
                    timeout=5
                )

                if result.returncode == 0:
                    # Скачиваем файл
                    subprocess.run(
                        ["adb", "pull", "/sdcard/translate.png", "screenshot.png"],
                        capture_output=True
                    )
                    self.current_image = PILImage.open("screenshot.png")
                else:
                    # Используем fallback
                    self.current_image = self.screen_capture.capture_screen_fallback()
            except:
                # Fallback способ
                self.current_image = self.screen_capture.capture_screen_fallback()

            if self.current_image:
                # Сохраняем временный файл для отображения
                self.current_image.save("current_screenshot.png")
                Clock.schedule_once(lambda dt: self._update_image_display(), 0)
                self.status_label.text = "Скриншот готов"
            else:
                self.status_label.text = "Ошибка при захвате"

        thread = threading.Thread(target=capture_thread, daemon=True)
        thread.start()

    def _update_image_display(self):
        """Обновляет отображение изображения"""
        if self.current_image:
            # Масштабируем изображение для отображения
            display_width = 380
            ratio = display_width / self.current_image.width
            display_height = int(self.current_image.height * ratio)

            resized = self.current_image.resize((display_width, display_height))
            resized.save("display_screenshot.png")

            self.image_display.source = "display_screenshot.png"
            self.image_display.reload()

    def translate_screenshot(self, instance=None):
        """Переводит текст со скриншота"""
        if not self.current_image:
            self.status_label.text = "Нет скриншота для перевода"
            return

        self.status_label.text = "Распознаю текст..."
        self.is_translating = True

        def translate_thread():
            try:
                # Распознаём текст
                text_data = self.ocr_engine.extract_text_from_image(self.current_image)

                if not text_data:
                    Clock.schedule_once(lambda dt: setattr(self.status_label, 'text', 'Текст не найден'), 0)
                    return

                Clock.schedule_once(lambda dt: setattr(self.status_label, 'text', 'Переводу текст...'), 0)

                # Переводим текст
                translated_data = self.translator.translate_text_with_positions(text_data)

                # Создаём оверлей
                overlay = TranslateOverlay(translated_data, self.current_image)
                self.current_translated_image = overlay.get_image()

                # Сохраняем и отображаем
                self.current_translated_image.save("translated_screenshot.png")

                Clock.schedule_once(lambda dt: self._show_translated_image(), 0)
                Clock.schedule_once(lambda dt: setattr(self.status_label, 'text', 'Перевод завершён'), 0)

            except Exception as e:
                print(f"Ошибка перевода: {e}")
                Clock.schedule_once(lambda dt: setattr(self.status_label, 'text', f'Ошибка: {str(e)[:30]}'), 0)

            finally:
                self.is_translating = False

        thread = threading.Thread(target=translate_thread, daemon=True)
        thread.start()

    def _show_translated_image(self):
        """Показывает переведённое изображение"""
        if self.current_translated_image:
            # Масштабируем для отображения
            display_width = 380
            ratio = display_width / self.current_translated_image.width
            display_height = int(self.current_translated_image.height * ratio)

            resized = self.current_translated_image.resize((display_width, display_height))
            resized.save("display_translated.png")

            self.image_display.source = "display_translated.png"
            self.image_display.reload()

if __name__ == '__main__':
    app = TranslateApp()
    app.run()
