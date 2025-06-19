# generators/text_gen_gg.py

import vertexai
from vertexai.generative_models import GenerativeModel
import logging
from google.api_core.exceptions import ResourceExhausted
import time

# Настройка логирования
logger = logging.getLogger(__name__)


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
        logger.info("Инициализация генератора текста Google Cloud Gemini...")

        # Инициализация Vertex AI
        vertexai.init(project=project_id, location=location)

        # Используем более быструю модель Gemini 1.5 Flash
        self.model = GenerativeModel("gemini-1.5-flash")
        self.tone = tone
        self.topic = topic
        logger.info("Текстовый генератор готов к работе.")

    def _generate_content(self, system_prompt: str, user_prompt: str, max_retries: int = 3) -> str | None:
        """
        Общий метод для генерации контента с обработкой ошибок и повторными попытками.

        Args:
            system_prompt (str): Системная инструкция
            user_prompt (str): Пользовательский запрос
            max_retries (int): Максимальное количество попыток

        Returns:
            str | None: Сгенерированный текст
        """
        for attempt in range(max_retries):
            try:
                response = self.model.generate_content(
                    contents=[user_prompt],
                    generation_config={
                        "temperature": 0.7 if "описание" in system_prompt else 0.4,
                        "max_output_tokens": 2048
                    },
                    system_instruction=system_prompt
                )

                if response.text:
                    return response.text.strip().strip('"')
                else:
                    logger.warning(f"Пустой ответ от Gemini (попытка {attempt + 1}/{max_retries})")

            except ResourceExhausted:
                wait_time = (attempt + 1) * 5  # Экспоненциальная задержка
                logger.warning(f"Достигнут лимит квот. Повтор через {wait_time} сек...")
                time.sleep(wait_time)
            except Exception as e:
                logger.error(f"Ошибка генерации: {e}")
                return None

        logger.error(f"Не удалось получить ответ после {max_retries} попыток")
        return None

    def generate_post(self) -> str | None:
        """
        Генерирует текст поста для социальных сетей.
        """
        system_prompt = f"Ты высококвалифицированный SMM специалист, который генерирует тексты для постов. Тон сообщений: {self.tone}."
        user_prompt = f"Сгенерируй пост для соцсетей на тему: '{self.topic}'. Пост должен быть привлекательным, содержательным и соответствовать тону {self.tone}."

        logger.info(f"Генерация поста: тема='{self.topic}', тон='{self.tone}'")
        return self._generate_content(system_prompt, user_prompt)

    def generate_post_image_description(self) -> str | None:
        """
        Генерирует детализированный промпт для модели генерации изображений.
        """
        system_prompt = (
            "Ты — эксперт по созданию промптов для генерации изображений. Генерируй только англоязычные промпты для моделей типа Imagen или Midjourney. "
            "Промпт должен включать: объект, окружение, стиль, освещение, детали. Пример: "
            "'photo of a sleek, modern kitchen knife with Damascus steel pattern, resting on dark granite next to chopped vegetables, cinematic lighting, ultra-realistic, 8k'."
        )
        user_prompt = f"Создай промпт для генерации изображения на тему: '{self.topic}'."

        logger.info(f"Генерация промпта для изображения: тема='{self.topic}'")
        return self._generate_content(system_prompt, user_prompt)