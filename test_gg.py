# test_gg.py

# Импортируем наши обновленные классы из Google-экосистемы
from generators.text_gen_gg import GeminiPostGenerator
from generators.image_gen_gg import ImagenGenerator
import config as conf

# --- Инициализация генератора текста Gemini ---
post_gen = GeminiPostGenerator(
    project_id=conf.GCP_PROJECT_ID,
    location=conf.GCP_LOCATION,
    tone="позитивный и весёлый",
    topic="Новая коллекция кухонных ножей от компании ZeroKnifes"
)
print("Генерация текста поста с помощью Gemini...")
content = post_gen.generate_post()

print("\nГенерация описания для изображения с помощью Gemini...")
img_desc = post_gen.generate_post_image_description()


# --- Инициализация генератора изображений Imagen ---
# Эта часть остается без изменений
img_gen = ImagenGenerator(
    project_id=conf.GCP_PROJECT_ID,
    location=conf.GCP_LOCATION,
    gcs_bucket_name=conf.GCS_BUCKET_NAME
)

print(f"\nГенерация изображения с помощью Imagen по сгенерированному промпту...")
print(f"Промпт для Imagen: {img_desc}")
image_url = img_gen.generate_image(img_desc)


# --- Вывод финального результата ---
print("\n" + "="*20 + " ГОТОВЫЙ ПОСТ " + "="*20)
print("\nТекст поста:\n")
print(content)
print("\nURL сгенерированного изображения:\n")
print(image_url)
print("\n" + "="*54)