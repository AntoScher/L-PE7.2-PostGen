import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from generators.image_gen_gg import ImagenGenerator
import config as conf


def test_image_generation():
    """Тестирование генерации изображений"""
    print("\n=== Тест генератора изображений ===")

    # Инициализация генератора
    img_gen = ImagenGenerator(
        project_id=conf.GCP_PROJECT_ID,
        location=conf.GCP_LOCATION,
        gcs_bucket_name=conf.GCS_BUCKET_NAME
    )

    # Тестовые промпты
    test_prompts = [
        "Красная панда на скейтборде в парке",
        "Футуристический город с летающими автомобилями",
        "Космическая станция на орбите Земли"
    ]

    for prompt in test_prompts:
        print(f"\nТестирование промпта: '{prompt}'")
        image_url = img_gen.generate_image(prompt)

        if image_url:
            print(f"✅ Успех! URL изображения: {image_url}")

            # Проверка локального сохранения
            local_files = os.listdir("generated_images")
            if any(prompt[:10] in f for f in local_files):
                print(f"✅ Локальный файл найден в generated_images/")
            else:
                print("❌ Локальный файл НЕ найден")
        else:
            print("❌ Ошибка генерации изображения")


if __name__ == "__main__":
    # Создание директории для изображений
    os.makedirs("generated_images", exist_ok=True)

    # Запуск тестов
    test_image_generation()
    print("\nТестирование завершено. Проверьте папку 'generated_images'")