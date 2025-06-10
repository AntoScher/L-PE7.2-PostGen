# generators/image_gen_gg.py

import os
import vertexai
from vertexai.preview.vision_models import ImageGenerationModel
from google.cloud import storage
from datetime import datetime, timedelta
from PIL import Image


class ImagenGenerator:
    """
    Класс для генерации изображений с использованием Google Cloud Imagen.
    """

    def __init__(self, project_id: str, location: str, gcs_bucket_name: str):
        """
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