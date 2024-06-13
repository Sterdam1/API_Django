import requests

def get_tokens(username, password):
    """
    Функция для получения токенов обновления и аторизации
    """

    url = "http://localhost:8000/api/token/"
    data = {
        "username": username,
        "password": password
    }

    response = requests.post(url, data=data)
    if 'access' in response.json():
        tokens = response.json()
        return tokens
    else:
        return f'Error, {response.json()["details"]}'

def get_all_users(headers):
    """
    Функция для полчения всех пользователей. Доступна только суперпользователю
    """

    url = "http://localhost:8000/api/users/"

    response = requests.get(url, headers=headers)
    return response.json()

def get_cur_user(headers):
    """
    Функция для получения информации о текущем пользователе
    """

    url = "http://localhost:8000/api/users/me/"

    response = requests.get(url, headers=headers)
    return f'ABOUT ME\n{response.json()}\n'

def create_user(data, headers):
    """
    Функция для создания нового пользователя

    Пример data
    data = {
        "username": "dark",
        "password": "darkspassword",
        "email": "dark@example.com",
        "phone": "1233211233",
        "user_type": "employee" client для клиента
    }
    """

    url = "http://localhost:8000/api/users/"

    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 201:
        return f'New user is {response.json()}'
    else:
        return f'Error {response.status_code}, {response.text}'
    
def get_all_tasks(headers):
    """
    Функция для получения всех задач
    """

    url = "http://localhost:8000/api/tasks/"

    response = requests.get(url, headers=headers)
    return response.json()

def get_exact_task(headers, task_id):
    """
    Функция для получение инфы о конкретной задаче
    """

    url = f"http://localhost:8000/api/tasks/{task_id}"

    response = requests.get(url, headers=headers)
    return response.json()

def create_task(data, headers):
    """
    Функция для создания новой задачи
    
    Пример data
    data = {
        "title": "Новая задача",
        "description": "Описание новой задачи"
    }
    """

    url = "http://localhost:8000/api/tasks/"

    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 201:
        task = response.json()
        print("Задача успешно создана:")
        return task
    else:
        print("Ошибка при создании задачи:", response.status_code, response.text)

def edit_task(data, headers, task_id):
    """
    Функция для изменения задачи

    Пример data
    data = {
        "title": "Новое название" необязательное поле
        "description": "Сделать проект" необязательное поле
    }
    """

    url = f"http://localhost:8000/api/tasks/{task_id}/"

    response = requests.patch(url, json=data, headers=headers)
    if response.status_code == 200:
        task = response.json()
        print("Задача успешно обновлена")
        return task
    else:
        print("Ошибка при редактировании задачи:", response.status_code, response.text)

def assign_task(task_id, headers):
    """
    Функция взятие задачи
    """

    url = f"http://localhost:8000/api/tasks/{task_id}/assign/"

    response = requests.post(url, headers=headers)

    if response.status_code == 200:
        task = response.json()
        print("Задача успешно назначена")
        return task
    else:
        print("Ошибка при назначении задачи:", response.status_code, response.text)


def close_task(task_id, headers, description):
    """
    Функция закрытия задачи
    """

    url = f"http://localhost:8000/api/tasks/{task_id}/close/"

    data = {
        "report": description
    }

    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 200:
        task = response.json()
        print("Задача успешно закрыта")
        return task
    else:
        print("Ошибка при назначении задачи:", response.status_code, response.text)


def delete_user(headers, user_id):
    """
    Функция для разработчика
    """
    url = f'http://localhost:8000/api/users/delete/{user_id}/'

    response = requests.delete(url, headers=headers)
    if response.status_code == 204:
        print('Пользователь удален')

tokens_dark = get_tokens('dark', 'darkspassword')
tokens_sterdam = get_tokens('sterdam', '123456')

headers_dark = {
    "Authorization": f"Bearer {tokens_dark['access']}",
    "Content-Type": "application/json"
}
headers_sterdam = {
    "Authorization": f"Bearer {tokens_sterdam['access']}",
    "Content-Type": "application/json"
}

# Пример даты
data_client = {
    "username": "light", 
    "password": "lightspassword", 
    "email": "lights@example.com", 
    "phone": "3213213123", 
    "user_type": "client" 
}

new_user = create_user(data=data_client, headers=headers_dark)
print(new_user)

# new_task = create_task(headers=headers_dark, data={
#     'title': "Задача дарка",
#     'description': "Описание задачи дарка"
# })
# users = get_all_users(headers=headers)
# print(*users, sep='\n')

tasks = get_all_tasks(headers=headers_sterdam)
print(*tasks, sep='\n')

task = get_exact_task(headers=headers_dark, task_id=3)
print(task)
