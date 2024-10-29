import pytest
import requests

@pytest.mark.usefixtures("base_url1", "channel_id", "headers", "message_id")
def test_create_message_with_text_and_attachment(base_url1, channel_id, headers):
    url = f"{base_url1}/channels/{channel_id}/messages"
    files = {
        'files[0]': ('test_image.png', open('test_image.png', 'rb'))
    }
    data = {
        'content': "Калды Балды."
    }
    headers.pop('Content-Type', None)
    response = requests.post(url, headers=headers, files=files, data=data)
    
    assert response.status_code == 200, "Expected 200, but got a different status code."
    message_id = response.json().get('id')
    assert message_id is not None, "Message ID is None"
    assert 'attachments' in response.json(), "No attachments in the response"

    print("Тест 'Создание сообщения с текстом и вложением' пройден успешно!")

def test_get_message(base_url1, channel_id, headers, message_id):
    url = f"{base_url1}/channels/{channel_id}/messages/{message_id}"
    response = requests.get(url, headers=headers)
    assert response.status_code == 200
    assert response.json().get('id') == str(message_id)

    print("Тест 'Получение сообщения' пройден успешно!")

def test_get_messages_array(base_url1, channel_id, headers):
    url = f"{base_url1}/channels/{channel_id}/messages"
    params = {
        "limit": 50
    }
    response = requests.get(url, headers=headers, params=params)
    assert response.status_code == 200
    messages = response.json()
    assert isinstance(messages, list)
    assert len(messages) > 0

    print("Тест 'Получение массива сообщений' пройден успешно!")

def test_add_reaction(base_url1, channel_id, headers, message_id):
    emoji = "🔥"
    emoji_encoded = requests.utils.quote(emoji)
    url = f"{base_url1}/channels/{channel_id}/messages/{message_id}/reactions/{emoji_encoded}/@me"
    response = requests.put(url, headers=headers)
    assert response.status_code == 204

    print("Тест 'Добавление реакции' пройден успешно!")

def test_remove_reaction(base_url1, channel_id, headers, message_id):
    emoji = "🔥"
    emoji_encoded = requests.utils.quote(emoji)
    add_reaction_url = f"{base_url1}/channels/{channel_id}/messages/{message_id}/reactions/{emoji_encoded}/@me"
    requests.put(add_reaction_url, headers=headers)
    
    remove_reaction_url = f"{base_url1}/channels/{channel_id}/messages/{message_id}/reactions/{emoji_encoded}/@me"
    response = requests.delete(remove_reaction_url, headers=headers)
    assert response.status_code == 204

    print("Тест 'Удаление реакции' пройден успешно!")

def test_create_message_without_content(base_url1, channel_id, headers):
    url = f"{base_url1}/channels/{channel_id}/messages"
    data = {
        "content": ""
    }
    response = requests.post(url, headers=headers, json=data)
    assert response.status_code == 400, "Expected 400 for empty content, but got a different status code."
    print("Негативный тест 'Создание сообщения без контента' пройден успешно!")

def test_get_message_with_invalid_id(base_url1, channel_id, headers):
    invalid_message_id = "12345678901234567890"
    url = f"{base_url1}/channels/{channel_id}/messages/{invalid_message_id}"
    response = requests.get(url, headers=headers)
    assert response.status_code == 400, "Expected 400 for invalid message ID, but got a different status code."
    print("Негативный тест 'Получение сообщения с несуществующим ID' пройден успешно!")

def test_add_reaction_to_nonexistent_message(base_url1, channel_id, headers):
    invalid_message_id = "12345678901234567890"
    emoji = "🔥"
    emoji_encoded = requests.utils.quote(emoji)
    url = f"{base_url1}/channels/{channel_id}/messages/{invalid_message_id}/reactions/{emoji_encoded}/@me"
    response = requests.put(url, headers=headers)
    assert response.status_code == 400, "Expected 400 for adding reaction to nonexistent message, but got a different status code."
    print("Негативный тест 'Добавление реакции к несуществующему сообщению' пройден успешно!")

def test_remove_reaction_from_nonexistent_message(base_url1, channel_id, headers):
    invalid_message_id = "12345678901234567890"
    emoji = "🔥"
    emoji_encoded = requests.utils.quote(emoji)
    url = f"{base_url1}/channels/{channel_id}/messages/{invalid_message_id}/reactions/{emoji_encoded}/@me"
    response = requests.delete(url, headers=headers)
    assert response.status_code == 400, "Expected 400 for removing reaction from nonexistent message, but got a different status code."
    print("Негативный тест 'Удаление реакции от несуществующего сообщения' пройден успешно!")
