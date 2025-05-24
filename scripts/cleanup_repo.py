import os
import re

# Конфигурация: файлы или папки, которые считаются лишними
REDUNDANT_PATTERNS = [
    r".*\.bak$",    # Резервные копии
    r".*\.tmp$",    # Временные файлы
    r".*\.log$",    # Лог-файлы
    r".*__pycache__.*",  # Кэш Python
    r".*\.DS_Store$",  # Системные файлы macOS
    r"^\.idea.*",  # Конфигурация IDE
    r"^\.vscode.*",  # Конфигурация VS Code
]

def is_redundant(file_path):
    """Проверяет, является ли файл или папка лишними на основе шаблонов."""
    for pattern in REDUNDANT_PATTERNS:
        if re.match(pattern, file_path):
            return True
    return False

def scan_and_cleanup(directory="."):
    """Сканирует директорию и удаляет лишние файлы."""
    for root, dirs, files in os.walk(directory):
        for name in files + dirs:
            path = os.path.join(root, name)
            relative_path = os.path.relpath(path, directory)

            if is_redundant(relative_path):
                print(f"Удаление: {relative_path}")
                if os.path.isfile(path):
                    os.remove(path)
                elif os.path.isdir(path):
                    os.rmdir(path)

if __name__ == "__main__":
    print("Автоматическая очистка репозитория...")
    scan_and_cleanup()
    print("Очистка завершена.")
