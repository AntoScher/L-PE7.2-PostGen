# test_ds_gg.py

from generators.text_gen_ds import DeepSeekPostGenerator
from generators.image_gen_gg import ImagenGenerator
import config as conf

# Инициализация генератора текста
post_gen = DeepSeekPostGenerator(
    api_key=conf.DEEPSEEK_API_KEY,
    tone="позитивный и весёлый",
    topic="Новая коллекция кухонных ножей от компании ZeroKnifes"
)

# Генерация контента
content = post_gen.generate_post()
img_desc = post_gen.generate_post_image_description()

# Инициализация генератора изображений (можно оставить как есть)
img_gen = ImagenGenerator(
    project_id=conf.GCP_PROJECT_ID,
    location=conf.GCP_LOCATION,
    gcs_bucket_name=conf.GCS_BUCKET_NAME
)

# Генерация изображения
image_url = img_gen.generate_image(img_desc)

# Вывод результатов
print("\nТекст поста:\n", content)
print("\nПромпт для изображения:\n", img_desc)
print("\nURL изображения:\n", image_url)