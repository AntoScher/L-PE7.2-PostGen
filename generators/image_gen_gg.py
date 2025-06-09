import google.generativeai as genai
import base64

class ImageGenerator:
    def __init__(self, google_api_key):
        """
        Инициализация генератора изображений с использованием Google Gemini API
        """
        genai.configure(api_key=google_api_key)
        self.model = genai.GenerativeModel('gemini-pro-vision')

    def generate_image(self, prompt):
        """
        Генерирует изображение на основе текстового промпта.
        Возвращает base64 строку с изображением в формате PNG.
        """
        try:
            # Генерация изображения
            response = self.model.generate_content(
                contents=[prompt],
                generation_config=genai.types.GenerationConfig(
                    candidate_count=1,
                    max_output_tokens=2048,
                    temperature=0.5
                )
            )

            # Проверка наличия изображения в ответе
            if not response.candidates or not response.candidates[0].content.parts:
                raise ValueError("API не вернуло изображение")

            # Извлечение изображения
            image_part = next((part for part in response.candidates[0].content.parts if part.mime_type.startswith('image/')), None)

            if not image_part:
                raise ValueError("В ответе не найдено данных изображения.")

            image_data = image_part.data
            image_mime_type = image_part.mime_type

            # Преобразование в base64
            image_base64 = base64.b64encode(image_data).decode('utf-8')
            return f"data:{image_mime_type};base64,{image_base64}"

        except Exception as e:
            print(f"Ошибка при генерации изображения: {e}")
            raise
