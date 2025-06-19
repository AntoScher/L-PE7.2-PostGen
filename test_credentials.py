import os
import sys
import json
import config as conf

def check_google_credentials():
    """Проверка учетных данных Google Cloud"""
    print("\n" + "="*50)
    print("Проверка учетных данных Google Cloud")
    print("="*50)

    # 1. Проверка переменной окружения
    creds_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    if not creds_path:
        print("❌ ОШИБКА: Переменная GOOGLE_APPLICATION_CREDENTIALS не установлена!")
        print("   Решение: Установите переменную окружения командой:")
        print("   Windows: $env:GOOGLE_APPLICATION_CREDENTIALS=\"D:\\path\\to\\service-account.json\"")
        print("   Linux/Mac: export GOOGLE_APPLICATION_CREDENTIALS=\"/path/to/service-account.json\"")
        return False

    print(f"✅ Переменная окружения: {creds_path}")

    # 2. Проверка существования файла
    if not os.path.exists(creds_path):
        print(f"❌ ОШИБКА: Файл сервисного аккаунта не найден: {creds_path}")
        return False

    print(f"✅ Файл сервисного аккаунта существует")

    # 3. Проверка содержимого файла
    try:
        with open(creds_path, 'r') as f:
            service_account = json.load(f)

        required_keys = ["type", "project_id", "private_key_id", "private_key", "client_email"]
        missing_keys = [key for key in required_keys if key not in service_account]

        if missing_keys:
            print(f"❌ ОШИБКА: В файле отсутствуют обязательные ключи: {', '.join(missing_keys)}")
            return False

        print(f"✅ Файл содержит все необходимые ключи")
        print(f"   Project ID: {service_account['project_id']}")
        print(f"   Client Email: {service_account['client_email']}")
        return True

    except json.JSONDecodeError:
        print("❌ ОШИБКА: Файл сервисного аккаунта содержит невалидный JSON")
        return False
    except Exception as e:
        print(f"❌ ОШИБКА при чтении файла: {str(e)}")
        return False

def check_config():
    """Проверка конфигурационного файла config.py"""
    print("\n" + "="*50)
    print("Проверка конфигурации config.py")
    print("="*50)

    required_vars = ["GCP_PROJECT_ID", "GCP_LOCATION", "GCS_BUCKET_NAME"]
    errors = []

    for var in required_vars:
        if not hasattr(conf, var):
            errors.append(f"❌ Отсутствует переменная: {var}")
        else:
            value = getattr(conf, var)
            if not value or value == "your-project-id":
                errors.append(f"❌ Переменная {var} не настроена")
            else:
                print(f"✅ {var} = {value}")

    if errors:
        for error in errors:
            print(error)
        print("\nРешение: Заполните все обязательные переменные в config.py")
        return False

    print("✅ Все обязательные переменные настроены")
    return True

def main():
    """Основная функция проверки"""
    credentials_ok = check_google_credentials()
    config_ok = check_config()

    print("\n" + "="*50)
    print("Итоговая проверка:")
    print("="*50)

    if credentials_ok and config_ok:
        print("✅ Все учетные данные настроены корректно!")
        print("   Можете запускать тесты и основное приложение")
        return True
    else:
        print("❌ Обнаружены проблемы с настройкой:")
        if not credentials_ok:
            print("   - Проблемы с учетными данными Google Cloud")
        if not config_ok:
            print("   - Проблемы с конфигурацией config.py")

        print("\n⚠️ Исправьте ошибки перед запуском приложения")
        return False

if __name__ == "__main__":
    if main():
        sys.exit(0)
    else:
        sys.exit(1)