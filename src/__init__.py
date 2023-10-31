import sys
import os

# Получаем путь к текущему каталогу (корневому каталогу проекта)
project_root = os.path.abspath(os.path.dirname(__file__))

# Добавляем корневой каталог проекта в sys.path
sys.path.insert(0, project_root)
