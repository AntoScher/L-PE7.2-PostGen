# test_text_gen_ds.py

from generators.text_gen_ds import DeepSeekPostGenerator
import config as conf

def test_deepseek_post_generator():
    print("🚀 Запуск тестирования DeepSeekPostGenerator...")

    # Инициализация генератора
    generator = DeepSeekPostGenerator(
        api_key=conf.DEEPSEEK_API_KEY,
        tone="позитивный и весёлый",
        topic="Новая коллекция кухонных ножей от компании ZeroKnifes"
    )

    print("\n📝 Тест: Генерация текстового поста...")
    post = generator.generate_post()
    if post:
        print("✅ Успешно сгенерирован пост:")
        print(post)
    else:
        print("❌ Не удалось сгенерировать пост.")

    print("\n🖼️ Тест: Генерация описания изображения...")
    image_prompt = generator.generate_post_image_description()
    if image_prompt:
        print("✅ Успешно сгенерирован промпт для изображения:")
        print(image_prompt)
    else:
        print("❌ Не удалось сгенерировать промпт для изображения.")

if __name__ == "__main__":
    test_deepseek_post_generator()