#!/bin/bash

set -e  # Прервать выполнение при любой ошибке

echo "🔍 Поиск pip или pip3..."

# Определяем, какой pip доступен
if command -v pip3 &> /dev/null; then
    PIP_CMD="pip3"
elif command -v pip &> /dev/null; then
    PIP_CMD="pip"
else
    echo "❌ Не найден ни pip, ни pip3. Установите Python и pip."
    exit 1
fi

echo "✅ Используем: $PIP_CMD"

# Проверяем наличие requirements.txt
if [ ! -f "requirements.txt" ]; then
    echo "❌ Файл requirements.txt не найден в текущей директории."
    exit 1
fi

# Проверяем наличие converter.py
if [ ! -f "converter.py" ]; then
    sudo "$PIP_CMD" install -r requirements.txt
    echo "❌ Файл converter.py не найден."
    exit 1
fi

echo "📦 Установка зависимостей из requirements.txt..."
"$PIP_CMD" install -r requirements.txt

echo "🛠️ Установка PyInstaller (--onedir)..."
pyinstaller --onedir converter.py

echo "🛠️ Запуск PyInstaller ./dist/converter/converter [input.json] [output.csv]"

echo "✅ Сборка завершена! Исполняемый файл находится в dist/converter/"

echo "Тест сборки файла nested.json:"
cat nested.json

echo ""
echo "Process..."

./dist/converter/converter -in=nested.json
echo ""
echo "Результат output.csv:"
cat output.csv


echo "✅ ГОТОВО"
