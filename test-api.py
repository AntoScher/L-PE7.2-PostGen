import os
import openai
from openai import OpenAI

# Импорт ключа из конфигурационного файла
from config import openai_key


# Проверка через список моделей (не тратит токены)
def check_api_health():
    try:
        client = OpenAI(api_key=openai_key)
        models = client.models.list()
        print("✅ API работает! Доступные модели:")
        for model in models.data:
            print(f"- {model.id}")
        return True
    except Exception as e:
        print(f"❌ Ошибка подключения: {e}")
        return False


# Альтернативный метод с минимальным запросом
def minimal_check():
    try:
        client = OpenAI(api_key=openai_key)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": "ping"}],
            max_tokens=1  # минимальное использование
        )
        print("✅ API отвечает. Статус:", response.status)
        return True
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False


# Запуск проверки
if __name__ == "__main__":
    print("Проверка через список моделей:")
    check_api_health()

    # Раскомментируйте для альтернативной проверки
#print("\nПроверка через минимальный запрос:")
#minimal_check()