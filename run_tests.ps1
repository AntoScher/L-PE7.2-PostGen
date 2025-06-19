#""".\run_tests.ps1"""#
# Установка переменной окружения
$env:GOOGLE_APPLICATION_CREDENTIALS = "D:\jobs-1_12_18\Pro_PYT\Промптинг\Модуль 7 . Кейсы\zc-dodiddone-431113-935c53d83975.json"

# Последовательный запуск тестов
Write-Host "Запуск проверки учетных данных..." -ForegroundColor Cyan
python test_credentials.py

if ($LASTEXITCODE -eq 0) {
    Write-Host "Учетные данные в порядке. Запуск тестов..." -ForegroundColor Green

    Write-Host "`nТест генератора текста:" -ForegroundColor Yellow
    python test_text_gen.py

    Write-Host "`nТест генератора изображений:" -ForegroundColor Yellow
    python test_image_gen.py

    Write-Host "`nИнтеграционный тест:" -ForegroundColor Yellow
    python test_gg.py
}
else {
    Write-Host "Обнаружены проблемы с учетными данными. Исправьте ошибки перед запуском тестов." -ForegroundColor Red
}

# Оставить окно открытым
Write-Host "`nНажмите Enter для выхода..." -ForegroundColor Gray
Read-Host