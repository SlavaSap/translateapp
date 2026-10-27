# 🚀 Как быстро получить APK

## За 5 шагов:

### 1️⃣ Залить на GitHub (2 минуты)

```bash
cd TranslateApp
git init
git add .
git commit -m "Translate App"
git remote add origin https://github.com/YOUR_USERNAME/translateapp.git
git push -u origin main
```

### 2️⃣ Включить Actions (1 минута)

1. GitHub.com → ваш репозиторий
2. Вкладка **Actions** → нажмите "I understand..."
3. Workflow **Build APK** → готов!

### 3️⃣ Запустить сборку (15 минут)

1. Actions → Build APK
2. Кнопка **Run workflow**
3. Выберите **main** branch
4. **Run workflow**

⏳ Ждем 10-15 минут...

### 4️⃣ Скачать APK (1 минута)

1. Actions → закончившийся workflow
2. **Artifacts** → **translate-app-apk**
3. Скачайте ZIP
4. Распакуйте `TranslateApp-debug.apk`

### 5️⃣ Установить на телефон (2 минуты)

**Если есть USB:**
```bash
adb install TranslateApp-debug.apk
```

**Если нет USB:**
1. Отправьте APK по Telegram/Viber
2. Откройте на телефоне
3. "Установить" → разрешите неизвестные источники
4. Готово! ✅

---

## 🎯 Что дальше?

Откройте приложение и:
1. Нажмите "Начать слушание"
2. Скажите: **"ТРАНСЛЕЙТ"**
3. Приложение захватит скрин и переведет! 🎉

---

## ❓ Если возникли проблемы

Читайте полную инструкцию: **INSTALL_ANDROID.md**
