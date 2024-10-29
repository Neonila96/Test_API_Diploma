import requests
import os
from dotenv import load_dotenv
import pytest
import allure

load_dotenv()

@pytest.fixture(scope="module")
def base_url1():
    return "https://discord.com/api/v10"


@pytest.fixture(scope="module")
def channel_id():
    return 1286673475565518878


@pytest.fixture(scope="module")
def get_headers():
    # Получаем токен из переменной окружения
    token = os.getenv('TOKEN')
    if not token:
        raise ValueError("Токен не найден. Убедитесь, что переменная окружения TOKEN задана.")

    # Создаем заголовки для запроса
    headers = {
        'Authorization': f"Bot {token}",
        'Content-Type': 'application/json'
    }

    # Логируем заголовки, скрывая токен
    headers_to_log = headers.copy()
    headers_to_log['Authorization'] = 'Bot [REDACTED]'
    allure.attach(str(headers_to_log), name="Request Headers", attachment_type=allure.attachment_type.TEXT)
    
    return headers

@pytest.fixture
def message_id(base_url1, channel_id, headers):
    # Создание сообщения перед каждым тестом
    url = f"{base_url1}/channels/{channel_id}/messages"
    data = {
        "content": "Калды Балды."
    }
    response = requests.post(url, headers=headers, json=data)
    assert response.status_code == 200, f"Failed to create message: {response.text}"
    message_id = response.json().get('id')
    yield message_id  # Возвращаем message_id для использования в тестах

    # Удаление сообщения после теста
    delete_url = f"{base_url1}/channels/{channel_id}/messages/{message_id}"
    response = requests.delete(delete_url, headers=headers)
    assert response.status_code == 204, f"Failed to delete message: {response.text}"
