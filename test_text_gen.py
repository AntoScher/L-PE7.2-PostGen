# test_text_gen.py

import os
import sys
import logging

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from generators.text_gen_gg import GeminiPostGenerator
import config as conf

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def test_text_generation():
    """Тестирование генерации текста и описания изображения"""
    print("\n=== Тест генератора текста ===")

    # Инициализация генератора
    post_gen = GeminiPostGenerator(
        project_id=conf.GCP_PROJECT_ID,
        location=conf.GCP_LOCATION,
        tone="позитивный и весёлый",
        topic="Новая коллекция кухонных ножей от компании ZeroKnifes"
    )

    # Генерация поста
    print("\nГенерация текста поста...")
    post_text = post_gen.generate_post()

    if post_text:
        print("✅ Успех! Текст поста:")
        print(post_text)
    else:
        print("❌ Ошибка генерации текста поста")
        return

    # Генерация описания изображения
    print("\nГенерация описания изображения...")
    img_desc = post_gen.generate_post_image_description()

    if img_desc:
        print("✅ Успех! Описание изображения:")
        print(img_desc)

        # Проверка, что описание на английском
        if all(ord(c) < 128 for c in img_desc):
            print("✅ Описание на английском языке")
        else:
            print("❌ Ошибка: описание должно быть на английском")
    else:
        print("❌ Ошибка генерации описания изображения")


if __name__ == "__main__":
    test_text_generation()
    print("\nТестирование завершено.")