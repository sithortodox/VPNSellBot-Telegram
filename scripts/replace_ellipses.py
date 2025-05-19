#!/usr/bin/env python3
import re
from pathlib import Path

# Шаблон: строка, состоящая только из "..."
PATTERN = re.compile(r'^(\s*)\.\.\.\s*$', flags=re.MULTILINE)

def replace_in_file(path: Path) -> bool:
    """
    Заменяет все строки, содержащие только '...', на 
    raise NotImplementedError("Не реализовано")
    Возвращает True, если файл был изменён.
    """
    text = path.read_text(encoding='utf-8')
    new_text = PATTERN.sub(r'\1raise NotImplementedError("Не реализовано")', text)
    if new_text != text:
        path.write_text(new_text, encoding='utf-8')
        return True
    return False

def main():
    changed = False
    for py_file in Path('.').rglob('*.py'):
        if replace_in_file(py_file):
            print(f"Fixed ellipsis in {py_file}")
            changed = True
    if not changed:
        print("No bare ellipses found.")

if __name__ == "__main__":
    main()
