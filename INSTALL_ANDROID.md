# Установка на Android

## 🚀 Способ 1: GitHub Actions (облачная сборка) - РЕКОМЕНДУЕТСЯ

### Шаг 1: Залить проект на GitHub

```bash
# Инициализируем git репозиторий
git init
git add .
git commit -m "Initial commit - Translate App"

# Добавляем远程 репозиторий (замените на ваш)
git remote add origin https://github.com/YOUR_USERNAME/translateapp.git
git branch -M main
git push -u origin main
```

### Шаг 2: Сборка в облаке

1. Зайдите на GitHub.com в ваш репозиторий
2. Откройте вкладку **Actions**
3. Выберите workflow **Build APK**
4. Нажмите **Run workflow**
5. Ждите ~10-15 минут

### Шаг 3: Скачиваем APK

1. Когда сборка закончится, откройте **Build APK** в Actions
2. Внизу увидите **Artifacts** → **translate-app-apk**
3. Скачайте ZIP файл
4. Распакуйте и найдите `.apk` файл

### Шаг 4: Установка на телефон

**Способ А (через USB):**
```bash
adb install -r TranslateApp-debug.apk
```

**Способ Б (ручная установка):**
1. Скопируйте APK на телефон (через облако, мессенджер или USB)
2. Откройте файловый менеджер на телефоне
3. Найдите APK файл
4. Нажмите → "Установить"
5. Разрешите установку из неизвестных источников (если спросит)

---

## 💻 Способ 2: Локальная сборка (долгий процесс)

### Требования:

- Windows 10/11 (64-bit)
- 10+ ГБ свободного места
- 30+ минут времени
- Python 3.8+
- Java JDK 11+

### Шаг 1: Установка Android SDK

```bash
# Скачайте Android Studio с https://developer.android.com/studio
# Установите с параметром Android SDK

# После установки, установите нужные компоненты:
# Запустите SDK Manager в Android Studio
# Установите:
# - Android SDK Platform 31
# - Android SDK Build Tools 31.0.0
# - Android NDK 21.3.6528147
```

### Шаг 2: Установка Buildozer и зависимостей

```bash
pip install buildozer cython
pip install -r requirements.txt

# Для Windows нужны дополнительные инструменты:
pip install pycparser
```

### Шаг 3: Конфигурация переменных окружения

```bash
# Установите переменные окружения (замените на ваши пути):
set JAVA_HOME=C:\Program Files\Java\jdk1.8.0_401
set ANDROID_HOME=C:\Users\YOUR_USER\AppData\Local\Android\Sdk
set ANDROID_SDK_ROOT=%ANDROID_HOME%
```

### Шаг 4: Сборка APK

```bash
cd TranslateApp
buildozer android debug
```

⏳ Это займет 20-40 минут при первом запуске!

### Шаг 5: Установка на телефон

APK файл будет в `TranslateApp/bin/translateapp-0.1-debug.apk`

```bash
adb install -r bin/translateapp-0.1-debug.apk
```

---

## 📱 После установки на телефон

### Первый запуск:

1. Откройте приложение "Translate App"
2. Разрешите все требуемые разрешения:
   - ✓ Микрофон
   - ✓ Доступ к медиа
   - ✓ Доступ к экрану (для скриншотов)
   - ✓ Интернет

3. Нажмите "Начать слушание"
4. Произнесите: **"ТРАНСЛЕЙТ"**

### Использование:

- Разговаривайте четко в микрофон
- После команды приложение автоматически:
  1. Захватит скриншот
  2. Распознает текст
  3. Переведет на русский
  4. Покажет результат оверлеем

---

## 🔧 Решение проблем

### "Installation failed"
```bash
# Удалите старую версию
adb uninstall org.translateapp
# Установите заново
adb install bin/translateapp-0.1-debug.apk
```

### "Permission denied"
- Включите "Установка из неизвестных источников" в настройках безопасности
- Settings → Security → Unknown sources

### Приложение не запускается
- Закройте и откройте еще раз
- Перезагрузите телефон
- Удалите и переустановите

### Микрофон не работает
- Проверьте разрешение для приложения: Settings → Apps → Translate App → Permissions → Microphone
- Убедитесь, что микрофон не заблокирован
- Перезагрузите приложение

---

## 📊 Сравнение способов

| | GitHub Actions | Локальная сборка |
|---|---|---|
| Время | 10-15 мин | 30-40 мин |
| Сложность | ⭐⭐ | ⭐⭐⭐⭐⭐ |
| Требования | Интернет, GitHub | JDK, SDK, много места |
| Рекомендуемо | ✅ ДА | ❌ Только если нужны исправления |

**РЕКОМЕНДУЕТСЯ**: Используйте GitHub Actions - это намного проще!

---

## 🚨 Важно!

При первом запуске EasyOCR загружает большую модель (~1 ГБ).
- Это займет 1-3 минуты
- Нужно постоянное интернет соединение
- После этого модель кэшируется на телефоне
