
# generators/image_gen_gg.py

import os
import vertexai
from vertexai.preview.vision_models import ImageGenerationModel
from google.cloud import storage
from datetime import datetime, timedelta
from PIL import Image

import requests
import base64
import json


class ImageGenerator:
    def __init__(self, google_api_key):
        """
        Инициализация генератора изображений.
        Используется REST API для модели Gemini через endpoint v1beta.
        """
        self.api_key = google_api_key
        # Обновлённый endpoint с версией v1beta
        self.endpoint = "https://generativeai.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"



class ImagenGenerator:
    """
    Класс для генерации изображений с использованием Google Cloud Imagen.
    """

    def __init__(self, project_id: str, location: str, gcs_bucket_name: str):
        """
<<<<<<< Updated upstream
        Инициализирует SDK Vertex AI, GCS клиент и загружает модель Imagen.
        Аутентификация должна быть настроена через переменную окружения
        GOOGLE_APPLICATION_CREDENTIALS.

        Args:
            project_id (str): ID проекта в Google Cloud.
            location (str): Регион для выполнения запросов.
            gcs_bucket_name (str): Имя бакета в Google Cloud Storage.
        """
        print("Инициализация генератора изображений Google Cloud Imagen...")
        vertexai.init(project=project_id, location=location)

        self.storage_client = storage.Client(project=project_id)
        self.bucket = self.storage_client.bucket(gcs_bucket_name)

        self.model = ImageGenerationModel.from_pretrained("imagegeneration@006")
        print("Генератор готов к работе.")

    def generate_image(self, prompt: str) -> str | None:
        """
        Генерирует изображение, сохраняет его локально, загружает в GCS
        и возвращает временный публичный URL.

        Args:
            prompt (str): Текстовое описание для генерации изображения.

        Returns:
            str | None: Временный публичный URL или None в случае ошибки.
        """
        print(f"Imagen: получен запрос на генерацию по промпту: '{prompt}'")

        try:
            response = self.model.generate_images(
                prompt=prompt,
                number_of_images=1
            )
        except Exception as e:
            print(f"Ошибка при вызове API Vertex AI: {e}")
            return None

        if not response.images:
            print("Ошибка: API не вернуло изображений.")
            return None

        # Создаем директорию для сохранения, если её нет
        output_dir = "generated_images"
        os.makedirs(output_dir, exist_ok=True)

        # Создаем уникальное имя файла
        base_filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
        local_save_path = os.path.join(output_dir, base_filename)

        # 1. Сохранение локально
        pil_image = response.images[0]._pil_image.convert('RGB')
        pil_image.save(local_save_path, 'jpeg')
        print(f"Изображение сохранено локально: {local_save_path}")

        # 2. Загрузка в GCS
        gcs_object_name = f"project-images/{base_filename}"
        blob = self.bucket.blob(gcs_object_name)
        blob.upload_from_filename(local_save_path)
        print(f"Файл загружен в GCS: gs://{self.bucket.name}/{gcs_object_name}")

        # 3. Генерация и возврат Signed URL
        signed_url = blob.generate_signed_url(version="v4", expiration=timedelta(minutes=60))
        print("Временный URL успешно сгенерирован.")

        return signed_url

        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "contents": [prompt],
            "generationConfig": {
                "candidateCount": 1,
                "maxOutputTokens": 2048,
                "temperature": 0.5,
                # Указываем модальности ответа, чтобы в ответ пришли данные изображения
                "responseModalities": ["IMAGE", "TEXT"]
            }
        }

        response = requests.post(self.endpoint, headers=headers, json=payload)
        if response.status_code != 200:
            raise Exception(f"Ошибка API (HTTP {response.status_code}): {response.text}")

        data = response.json()

        # Для отладки: можно вывести полный ответ
        # print(json.dumps(data, indent=2))

        # Проверяем, что в ответе присутствуют кандидаты и части контента
        if not data.get("candidates") or not data["candidates"][0].get("content") or not data["candidates"][0][
            "content"].get("parts"):
            raise ValueError("API не вернуло ожидаемых данных")

        parts = data["candidates"][0]["content"]["parts"]

        # Ищем часть, содержащую изображение (определяем по MIME-типу)
        image_part = None
        for part in parts:
            mime = part.get("mime_type") or part.get("mimeType")
            if mime and mime.startswith("image/"):
                image_part = part
                break

        if not image_part:
            raise ValueError("В ответе не найдено данных изображения.")

        # Извлекаем данные изображения
        image_data = image_part["data"]
        # Если API возвращает бинарные данные, можно применить base64.b64encode,
        # однако зачастую данные уже возвращаются в виде base64-строки.
        return f"data:{mime};base64,{image_data}"
"""
