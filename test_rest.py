import requests
import json
from google.oauth2 import service_account
from google.auth.transport.requests import Request
import logging

# Настройка логирования
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Настройки
SERVICE_ACCOUNT_FILE = r"D:\DEV\L-PE7.2-PostGen\zc-dodiddone-431113-935c53d83975.json"
PROJECT_ID = "zc-dodiddone-431113"
LOCATION = "us-central1"  # Важно: только us-central1 для Gemini 1.5
MODEL_ID = "gemini-1.5-flash-001"  # Корректное имя модели


def main():
    try:
        # Аутентификация
        credentials = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE,
            scopes=["https://www.googleapis.com/auth/cloud-platform"]
        )

        if not credentials.valid:
            credentials.refresh(Request())
            logger.info("Токен обновлен")

        logger.info(f"Аутентификация успешна. Сервисный аккаунт: {credentials.service_account_email}")

        # Формирование запроса
        endpoint = f"https://{LOCATION}-aiplatform.googleapis.com/v1/projects/{PROJECT_ID}/locations/{LOCATION}/publishers/google/models/{MODEL_ID}:generateContent"

        headers = {
            "Authorization": f"Bearer {credentials.token}",
            "Content-Type": "application/json"
        }

        payload = {
            "contents": [{
                "role": "user",
                "parts": [{"text": "Ответь одним словом: столица Франции?"}]
            }]
        }

        logger.debug(f"Отправка запроса на: {endpoint}")
        logger.debug(f"Заголовки: {headers}")
        logger.debug(f"Тело запроса: {json.dumps(payload, indent=2)}")

        # Отправка запроса
        response = requests.post(endpoint, headers=headers, json=payload)

        logger.info(f"Код статуса: {response.status_code}")

        if response.status_code == 200:
            result = response.json()
            logger.info("Успешный ответ:")
            logger.info(json.dumps(result, indent=2))

            # Извлечение текста ответа
            try:
                text = result['candidates'][0]['content']['parts'][0]['text']
                logger.info(f"\nОтвет Gemini: {text}")
            except KeyError:
                logger.error("Не удалось извлечь текст из ответа")
        else:
            logger.error(f"Ошибка: {response.status_code}")
            logger.error(response.text)

    except Exception as e:
        logger.exception("Критическая ошибка")


if __name__ == "__main__":
    logger.info("Запуск теста REST API для Gemini")
    main()
    logger.info("Тест завершен")