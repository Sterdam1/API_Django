import requests
# ПОЛУЧЕНИЕ ТОКЕНА АДМИНА
url = "http://localhost:8000/api/token/"
data = {
    "username": "admin",
    "password": "admin"
}

response = requests.post(url, data=data)
tokens = response.json()

# print(f'TOKENS\n{tokens}\n')

headers = {
    "Authorization": f"Bearer {tokens['access']}",
    "Content-Type": "application/json"
}

# url = "http://localhost:8000/api/users/"

# ПОЛУЧЕНИЕ ТОКЕНА СОТРУДНИКОВ 
# data_employee = {
#     "username": "sterdam",
#     "password": "123456"
# }

# УДАЛЕНИЕ ПОЛЬЗОВАТЕЛЯ
# url = 'http://localhost:8000/api/users/delete/7/'

# response = requests.delete(url, headers=headers)
# if response.status_code == 204:
#     print('Пользователь удален')

# url = "http://localhost:8000/api/token/"

# response = requests.post(url, json=data_employee)
# print(response.json())
# tokens = response.json()

# headers = {
#     "Authorization": f"Bearer {tokens['access']}",
#     "Content-Type": "application/json"
# }

# url = f"http://localhost:8000/api/tasks/1/close/"
# data = {
#     "report": "Отчет о выполнении задачи"
# }
# response = requests.post(url, json=data, headers=headers)
# if response.status_code == 200:
#     task = response.json()
#     print("Задача успешно закрыта:", task)
# else:
#     print("Ошибка при закрытии задачи:", response.status_code, response.text)

url = "http://localhost:8000/api/users/"
response = requests.get(url, headers=headers)
print(*response.json(), sep='\n') #О ВСЕХ ПОЛЬЗОВАТЕЛЯХ(ADMIN)

url = "http://localhost:8000/api/tasks/"

response = requests.get(url, headers=headers)
print('ВСЕ ЗАДАЧИ')
print(*response.json(), sep='\n\n')

# ПОЛУЧЕНИЕ ИНФЫ О ПОЛЬЗОВАТЕЛЕ
# url = "http://localhost:8000/api/users/me/"
# # url = "http://localhost:8000/api/users/" О ВСЕХ ПОЛЬЗОВАТЕЛЯХ(ADMIN)

# response = requests.get(url, headers=headers)
# print(f'ABOUT ME\n{response.json()}\n')
# print(*response.json(), sep='\n') #О ВСЕХ ПОЛЬЗОВАТЕЛЯХ(ADMIN)


# ПРОСМОТР ВСЕХ ЗАДАЧ
# url = "http://localhost:8000/api/tasks/"

# response = requests.get(url, headers=headers)
# print('ВСЕ ЗАДАЧИ')
# print(*response.json(), sep='\n\n')

# НОВАЯ ЗАДАЧА
# data = {
#     "title": "Новая задача",
#     "description": "Описание новой задачи"
# }

# response = requests.post(url, json=data, headers=headers)

# if response.status_code == 201:
#     task = response.json()
#     print("Задача успешно создана:", task)
# else:
#     print("Ошибка при создании задачи:", response.status_code, response.text)

# РЕДАКТИРОВАНИЕ ЗАДАЧИ
# url = f"http://localhost:8000/api/tasks/1/"
# data = {
#     "description": "Сделать проект"
# }

# response = requests.patch(url, json=data, headers=headers)

# if response.status_code == 200:
#     task = response.json()
#     print("Задача успешно обновлена:", task)
# else:
#     print("Ошибка при редактировании задачи:", response.status_code, response.text)

# ВЗЯТИЕ ЗАДАЧИ
# url = f"http://localhost:8000/api/tasks/{task_id}/assign/
# response = requests.post(url, headers=headers)
# # if response.status_code == 200:
#     task = response.json()
#     print("Задача успешно назначена:", task)
# else:
#     print("Ошибка при назначении задачи:", response.status_code, response.text)

# ЗАКРЫТИЕ ЗАДАЧИ
# url = f"http://localhost:8000/api/tasks/{task_id}/close/"
# data = {
#     "report": "Отчет о выполнении задачи"
# }
# response = requests.post(url, json=data, headers=headers)
# if response.status_code == 200:
#     task = response.json()
#     print("Задача успешно закрыта:", task)
# else:
#     print("Ошибка при закрытии задачи:", response.status_code, response.json())

# СОЗДАНИЕ СОТРУДНИКА И КЛИЕНТА
# url = "http://localhost:8000/api/users/"

# data_employee = {
#     "username": "dark",
#     "password": "darkspassword",
#     "email": "dark@example.com",
#     "phone": "1233211233",
#     "user_type": "employee" # client для клиента
# }

# data_client = {
#     "username": "light",
#     "password": "lightspassword",
#     "email": "light@example.com",
#     "phone": "0988900987",
#     "user_type": "client" # employee для клиента
# } 
# response_employee = requests.post(url, json=data_employee, headers=headers)
# response_client =  requests.post(url, json=data_client, headers=headers)

# print(f'NEW EMPLOYEE\n{response_employee.json()}\n')
# print(f'NEW CLIENT\n{response_client.json()}\n')

# ОБНОВЛЕНИЕ ДАННЫХ ПОЛЬЗОВАТЕЛЯ **НЕ НАДО
# url = "http://localhost:8000/api/users/1/"

# data = {
#     "email":"some@email.com"
# }

# response = requests.patch(url, json=data, headers=headers)

# if response.status_code == 200:
#     updated_user = response.json()
#     print("Пользователь успешно отредактирован:", updated_user)
# else:
#     print("Error:", response.status_code, response)