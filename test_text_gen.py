import os
import sys
import logging
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from generators.text_gen_gg import GeminiPostGenerator
import config as conf

# Детальное логирование
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


def test_basic_generation():
    """Проверка базовой работы Vertex AI"""
    logger.info("=== ТЕСТ БАЗОВОЙ ГЕНЕРАЦИИ ===")

    try:
        import vertexai
        from vertexai.generative_models import GenerativeModel

        vertexai.init(project=conf.GCP_PROJECT_ID, location=conf.GCP_LOCATION)
        model = GenerativeModel("gemini-1.5-flash-001")

        start_time = time.time()
        response = model.generate_content("Ответь одним словом: как называется столица Франции?")
        duration = time.time() - start_time

        if response.text.strip().lower() == "париж":
            logger.info(f"✅ Базовая генерация успешна! Ответ: {response.text} (за {duration:.2f} сек)")
            return True
        else:
            logger.error(f"❌ Неверный ответ: {response.text}")
            return False

    except Exception as e:
        logger.exception("🔥 Ошибка базовой генерации")
        return False


def test_text_generation():
    """Тестирование генерации текста и описания изображения"""
    logger.info("\n=== ТЕСТ ГЕНЕРАТОРА ТЕКСТА ===")

    # Инициализация генератора
    try:
        logger.info("Инициализация GeminiPostGenerator...")
        post_gen = GeminiPostGenerator(
            project_id=conf.GCP_PROJECT_ID,
            location=conf.GCP_LOCATION,
            tone="позитивный и весёлый",
            topic="Новая коллекция кухонных ножей от компании ZeroKnifes"
        )
        logger.info("Генератор инициализирован")
    except Exception as e:
        logger.exception("❌ Ошибка инициализации генератора")
        return

    # Генерация поста
    logger.info("Генерация текста поста...")
    start_time = time.time()
    post_text = post_gen.generate_post()
    duration = time.time() - start_time

    if post_text:
        logger.info(f"✅ Успех! Текст поста (сгенерирован за {duration:.2f} сек):")
        logger.info(post_text)
    else:
        logger.error("❌ Ошибка генерации текста поста")
        return

    # Генерация описания изображения
    logger.info("\nГенерация описания изображения...")
    start_time = time.time()
    img_desc = post_gen.generate_post_image_description()
    duration = time.time() - start_time

    if img_desc:
        logger.info(f"✅ Успех! Описание изображения (за {duration:.2f} сек):")
        logger.info(img_desc)

        # Проверка языка
        if all(ord(c) < 128 for c in img_desc):
            logger.info("✅ Описание на английском языке")
        else:
            logger.error("❌ Ошибка: описание должно быть на английском")
    else:
        logger.error("❌ Ошибка генерации описания изображения")


if __name__ == "__main__":
    logger.info("\n" + "=" * 50)
    logger.info("ЗАПУСК ТЕСТОВ ГЕНЕРАТОРА ТЕКСТА")
    logger.info("=" * 50)

    # Проверка базовой работы Vertex AI
    if not test_basic_generation():
        logger.error("🔥 Базовый тест не пройден! Дальнейшие тесты отменены.")
        exit(1)

    # Основной тест
    test_text_generation()

    logger.info("\n" + "=" * 50)
    logger.info("ТЕСТИРОВАНИЕ ЗАВЕРШЕНО")
    logger.info("=" * 50)