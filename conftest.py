import requests
import os
from dotenv import load_dotenv
import pytest

load_dotenv()

@pytest.fixture(scope="module")
def base_url1():
    return "https://discord.com/api/v10"


@pytest.fixture(scope="module")
def channel_id():
    return 1286673475565518878


@pytest.fixture(scope="module")
def headers():
    token = os.getenv("TOKEN")
    if not token:
        raise ValueError("Токен не найден. Убедитесь, что переменная окружения TOKEN задана.")
    return {
        "Authorization": f"Bot {token}",
        "Content-Type": "application/json"
    }


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
