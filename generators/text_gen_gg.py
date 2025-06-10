# generators/text_gen.py

import vertexai
from vertexai.generative_models import GenerativeModel, Part


class GeminiPostGenerator:
    """
    Класс для генерации текстового контента с помощью Google Cloud Gemini.
    """

    def __init__(self, project_id: str, location: str, tone: str, topic: str):
        """
        Инициализирует SDK Vertex AI и загружает модель Gemini.

        Args:
            project_id (str): ID проекта в Google Cloud.
            location (str): Регион для выполнения запросов.
            tone (str): Тон, в котором должен быть написан пост.
            topic (str): Тема поста.
        """
        print("Инициализация генератора текста Google Cloud Gemini...")

        # vertexai.init() вызывается один раз в основном скрипте,
        # но безопасно вызывать его повторно.
        # Чтобы избежать лишних сообщений, можно добавить проверку.
        try:
            vertexai.init(project=project_id, location=location)
        except ImportError:
            # Уже инициализирован
            pass

        # Загружаем последнюю версию модели Gemini 1.5 Pro
        self.model = GenerativeModel("gemini-1.5-pro-preview-0409")
        self.tone = tone
        self.topic = topic
        print("Текстовый генератор готов к работе.")

    def generate_post(self) -> str | None:
        """
        Генерирует текст поста для социальных сетей.
        """
        # Системные инструкции в Gemini передаются в поле `system_instruction`
        system_prompt = "Ты высококвалифицированный SMM специалист, который будет помогать в генерации текста для постов с заданной тематикой и заданным тоном."
        user_prompt = f"Сгенерируй пост для соцсетей с темой '{self.topic}', используя тон: {self.tone}. Пост должен быть содержательным и привлекательным для аудитории."

        try:
            # Передаем системный промпт отдельно для лучшего контроля
            model_with_system_prompt = GenerativeModel(
                "gemini-1.5-pro-preview-0409",
                system_instruction=system_prompt
            )
            response = model_with_system_prompt.generate_content(user_prompt)
            return response.text
        except Exception as e:
            print(f"Ошибка при генерации текста поста: {e}")
            return None

    def generate_post_image_description(self) -> str | None:
        """
        Генерирует детализированный промпт для модели генерации изображений.
        """
        system_prompt = (
            "Ты — ассистент по созданию промптов для нейросетей, генерирующих изображения (таких как Imagen или Midjourney). "
            "Твоя задача — составить очень детализированный, яркий и креативный промпт на английском языке для генерации изображения на заданную тему. "
            "Промпт должен включать описание объекта, окружения, стиля, освещения и деталей. "
            "Например: 'photo of a sleek, modern kitchen knife with a Damascus steel pattern on the blade, resting on a dark granite countertop next to freshly chopped vegetables, cinematic lighting, ultra-realistic, 8k'."
        )
        user_prompt = f"Создай такой промпт для темы: '{self.topic}'."

        try:
            model_with_system_prompt = GenerativeModel(
                "gemini-1.5-pro-preview-0409",
                system_instruction=system_prompt
            )
            response = model_with_system_prompt.generate_content(user_prompt)
            # Модель может вернуть промпт в кавычках, убираем их
            return response.text.strip().strip('"')
        except Exception as e:
            print(f"Ошибка при генерации описания изображения: {e}")
            return None
