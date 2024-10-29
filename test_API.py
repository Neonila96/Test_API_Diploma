import pytest
import requests


@pytest.mark.usefixtures("base_url1", "channel_id", "headers", "message_id")
# Тестирование создания сообщения с текстом и вложением
def test_create_message_with_text_and_attachment(base_url1, channel_id, headers):
    url = f"{base_url1}/channels/{channel_id}/messages"


    files = {
        'files[0]': ('test_image.png', open('test_image.png', 'rb'))
    }

    # Данные с текстом сообщения
    data = {
        'content': "Калды Балды."
    }


    headers.pop('Content-Type', None)

    # Отправка POST запроса с текстом и вложением
    response = requests.post(url, headers=headers, files=files, data=data)

    # Проверяем, что запрос прошел успешно
    assert response.status_code == 200, f"Expected 200, but got {response.status_code}: {response.text}"

    # Проверяем наличие ID сообщения
    message_id = response.json().get('id')
    assert message_id is not None, "Message ID is None"

    # Проверяем, что вложение присутствует в ответе
    assert 'attachments' in response.json(), "No attachments in the response"

    print("Тест 'Создание сообщения с текстом и вложением' пройден успешно!")


def test_get_message(base_url1, channel_id, headers, message_id):
    url = f"{base_url1}/channels/{channel_id}/messages/{message_id}"
    response = requests.get(url, headers=headers)
    assert response.status_code == 200
    assert response.json().get('id') == str(message_id)

    print("Тест 'Получение сообщения' пройден успешно!")


def test_get_messages_array(base_url1, channel_id, headers, message_id):
    url = f"{base_url1}/channels/{channel_id}/messages"
    params = {
        "limit": 50  # Получаем до 50 сообщений
    }
    response = requests.get(url, headers=headers, params=params)
    assert response.status_code == 200
    messages = response.json()
    assert isinstance(messages, list)
    assert len(messages) > 0  # Проверяем, что в канале есть сообщения

    print("Тест 'Получение массива сообщений' пройден успешно!")


def test_add_reaction(base_url1, channel_id, headers, message_id):
    emoji = "🔥"  # Эмодзи для реакции
    emoji_encoded = requests.utils.quote(emoji)  # URL-кодирование эмодзи
    url = f"{base_url1}/channels/{channel_id}/messages/{message_id}/reactions/{emoji_encoded}/@me"
    response = requests.put(url, headers=headers)
    assert response.status_code == 204  # Успешный код ответа

    print("Тест 'Добавление реакции' пройден успешно!")


#def test_remove_reaction(base_url1, channel_id, headers, message_id):
    emoji = "🔥"  # Эмодзи для реакции
    emoji_encoded = requests.utils.quote(emoji)  # URL-кодирование эмодзи
    # Сначала добавляем реакцию
    add_reaction_url = f"{base_url1}/channels/{channel_id}/messages/{message_id}/reactions/{emoji_encoded}/@me"
    requests.put(add_reaction_url, headers=headers)
    # Теперь удаляем реакцию
    remove_reaction_url = f"{base_url1}/channels/{channel_id}/messages/{message_id}/reactions/{emoji_encoded}/@me"
    response = requests.delete(remove_reaction_url, headers=headers)
    assert response.status_code == 204, f"Ожидался статус 204 для успешного удаления реакции, но получен {response.status_code}"

    print("Тест 'Удаление реакции' пройден успешно!")

def test_create_message_without_content(base_url1, channel_id, headers):
    url = f"{base_url1}/channels/{channel_id}/messages"
    data = {
        "content": ""  # Пустое сообщение
    }
    response = requests.post(url, headers=headers, json=data)
    assert response.status_code == 400, f"Expected 400 for empty content, but got {response.status_code}: {response.text}"
    print("Негативный тест 'Создание сообщения без контента' пройден успешно!")


def test_get_message_with_invalid_id(base_url1, channel_id, headers):
    invalid_message_id = "12345678901234567890"  # Не существующий ID
    url = f"{base_url1}/channels/{channel_id}/messages/{invalid_message_id}"
    response = requests.get(url, headers=headers)
    assert response.status_code == 400, f"Expected 400 for invalid message ID, but got {response.status_code}: {response.text}"
    print("Негативный тест 'Получение сообщения с несуществующим ID' пройден успешно!")


def test_add_reaction_to_nonexistent_message(base_url1, channel_id, headers):
    invalid_message_id = "12345678901234567890"  # Не существующий ID
    emoji = "🔥"
    emoji_encoded = requests.utils.quote(emoji)
    url = f"{base_url1}/channels/{channel_id}/messages/{invalid_message_id}/reactions/{emoji_encoded}/@me"
    response = requests.put(url, headers=headers)
    assert response.status_code == 400, "Expected 400 for adding reaction to nonexistent message, but got {}".format(response.status_code)
    print("Негативный тест 'Добавление реакции к несуществующему сообщению' пройден успешно!")


#def test_remove_reaction_from_nonexistent_message(base_url1, channel_id, headers):
    invalid_message_id = "12345678901234567890"  # Не существующий ID
    emoji = "🔥"
    emoji_encoded = requests.utils.quote(emoji)
    url = f"{base_url1}/channels/{channel_id}/messages/{invalid_message_id}/reactions/{emoji_encoded}/@me"
    response = requests.delete(url, headers=headers)
    assert response.status_code == 400, "Expected 400 for removing reaction from nonexistent message, but got {}".format(response.status_code)
    print("Негативный тест 'Удаление реакции от несуществующего сообщения' пройден успешно!")
