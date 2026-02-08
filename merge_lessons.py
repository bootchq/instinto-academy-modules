#!/usr/bin/env python3
"""Извлекает lessons из оригинального HTML и добавляет в v2."""

import re
from pathlib import Path

original = Path("/private/tmp/academy-modules/index.html").read_text(encoding='utf-8')
v2 = Path("/private/tmp/academy-modules/index-v2.html").read_text(encoding='utf-8')

# Находим объект lessons в оригинале
# Ищем от "const lessons = {" до закрывающей "        };"
match = re.search(r'(const lessons = \{[\s\S]*?\n        \};)', original)

if match:
    lessons_obj = match.group(1)
    print(f"Найден объект lessons, длина: {len(lessons_obj)} символов")

    # Заменяем placeholder в v2
    placeholder = '''    <script>
        // Copy lessons object from original index.html
        // This will be populated by the build script
    </script>'''

    new_script = f'''    <script>
        {lessons_obj}
    </script>'''

    v2_new = v2.replace(placeholder, new_script)

    Path("/private/tmp/academy-modules/index-v2.html").write_text(v2_new, encoding='utf-8')
    print("Обновлён index-v2.html")
else:
    print("Не найден объект lessons!")
