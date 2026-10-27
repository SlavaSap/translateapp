import speech_recognition as sr
import threading
from queue import Queue

class VoiceListener:
    def __init__(self, callback=None):
        self.recognizer = sr.Recognizer()
        self.callback = callback
        self.listening = False
        self.thread = None
        self.command_queue = Queue()

        # Установки распознавания
        self.recognizer.energy_threshold = 4000
        self.recognizer.dynamic_energy_threshold = True

    def start_listening(self):
        """Начинает слушать команду"""
        if self.listening:
            return

        self.listening = True
        self.thread = threading.Thread(target=self._listen_loop, daemon=True)
        self.thread.start()

    def stop_listening(self):
        """Останавливает слушание"""
        self.listening = False
        if self.thread:
            self.thread.join(timeout=2)

    def _listen_loop(self):
        """Основной цикл слушания"""
        try:
            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)

                while self.listening:
                    try:
                        # Слушаем аудио
                        audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=5)

                        # Пытаемся распознать текст
                        try:
                            text = self.recognizer.recognize_google(audio, language='ru-RU')
                            print(f"Распознано: {text}")

                            # Проверяем команду
                            if self._check_command(text):
                                self.command_queue.put(text)
                                if self.callback:
                                    self.callback(text)

                        except sr.UnknownValueError:
                            pass
                        except sr.RequestError as e:
                            print(f"Ошибка Google Speech: {e}")

                    except sr.RequestError:
                        continue

        except Exception as e:
            print(f"Ошибка слушания: {e}")

    def _check_command(self, text):
        """Проверяет, содержит ли текст команду"""
        text_lower = text.lower()

        # Проверяем варианты команды
        commands = ['транслейт', 'translate', 'переводить', 'перевод']
        return any(cmd in text_lower for cmd in commands)

    def get_command(self, timeout=None):
        """Получает команду из очереди"""
        try:
            return self.command_queue.get(timeout=timeout)
        except:
            return None
