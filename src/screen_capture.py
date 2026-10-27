from PIL import Image
import numpy as np
import os

class ScreenCapture:
    def __init__(self):
        self.last_screenshot = None

    def capture_screen(self):
        """Захватывает скрин устройства (для Android)"""
        try:
            import subprocess

            # Используем adb screencap для захвата скрина
            screenshot_path = "/sdcard/translate_screenshot.png"

            # Выполняем screencap
            result = subprocess.run(
                ["adb", "shell", "screencap", "-p", screenshot_path],
                capture_output=True,
                text=True
            )

            if result.returncode == 0:
                # Копируем файл на компьютер и открываем его
                local_path = os.path.expanduser("~/translate_screenshot.png")
                subprocess.run(["adb", "pull", screenshot_path, local_path])

                image = Image.open(local_path)
                self.last_screenshot = image
                return image
            else:
                print(f"Ошибка screencap: {result.stderr}")
                return None

        except Exception as e:
            print(f"Ошибка захвата экрана: {e}")
            return None

    def capture_screen_fallback(self):
        """Альтернативный способ захвата через Kivy"""
        try:
            from kivy.core.window import Window
            from kivy.graphics import Texture

            # Захватываем пиксели окна Kivy
            texture = Window.texture
            pixels = texture.pixels

            # Конвертируем в PIL Image
            width, height = Window.size
            image_data = np.frombuffer(pixels, dtype=np.uint8).reshape((height, width, 4))

            # Конвертируем RGBA в RGB
            image_rgb = image_data[:, :, :3]

            image = Image.fromarray(image_rgb)
            self.last_screenshot = image
            return image
        except Exception as e:
            print(f"Ошибка fallback скрина: {e}")
            return None

    def get_last_screenshot(self):
        """Возвращает последний захваченный скрин"""
        return self.last_screenshot

    def save_screenshot(self, filename="screenshot.png"):
        """Сохраняет скрин в файл"""
        if self.last_screenshot:
            self.last_screenshot.save(filename)
            return True
        return False
