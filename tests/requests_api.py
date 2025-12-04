import pytest
from httpx import AsyncClient
from unittest.mock import patch, AsyncMock
from sqlalchemy.exc import SQLAlchemyError
from src.schemas import CheckRequestSchema


# async def test_request_add(ac: AsyncClient):
#     response = await ac.post("/requests")
    
#     data = {"ip_address": "127.0.0.1", "prompt": "Hello World!"}
#     assert response.status_code == 200



async def test_create_my_request_success(ac: AsyncClient):
    # Подготавливаем тестовые данные
    test_prompt = "Тестовый запрос"
    test_response = "Тестовый ответ"
    test_ip = "127.0.0.1"
    
    # Мокаем функцию get_giga_response для возврата предсказуемого результата
    with patch('src.routers.requests.get_giga_response') as mock_giga:
        # Настраиваем мок так, чтобы он возвращал итератор с одним элементом
        mock_giga.return_value = iter([['a', 'b', 'c', test_response]])
        
        # Мокаем функцию add_request_data
        with patch('src.routers.requests.add_request_data') as mock_add:
            mock_add.return_value = None
            
            # Отправляем POST запрос
            response = await ac.post("/requests/", json={"prompt": test_prompt})
            
            # Проверяем статус код
            assert response.status_code == 201
            
            # Проверяем статус код
            assert response.status_code == 201
            
            # Проверяем структуру ответа
            response_data = response.json()
            assert "message" in response_data
            assert response_data["message"] == "Request created successfully"
            
            # Проверяем, что функции были вызваны с правильными аргументами
            mock_giga.assert_called_once_with(test_prompt)
            mock_add.assert_called_once()



async def test_create_my_request_with_x_forwarded_for(ac: AsyncClient):
    # Тест для случая, когда request.client равен None
    test_prompt = "Тестовый запрос"
    test_response = "Тестовый ответ"
    
    # Мокаем функцию get_giga_response
    with patch('src.routers.requests.get_giga_response') as mock_giga:
        mock_giga.return_value = iter([['a', 'b', 'c', test_response]])
        
        # Мокаем функцию add_request_data
        with patch('src.routers.requests.add_request_data') as mock_add:
            mock_add.return_value = None
            
            # Отправляем POST запрос с заголовком X-Forwarded-For
            response = await ac.post(
                "/requests/", 
                json={"prompt": test_prompt},
                headers={"X-Forwarded-For": "192.168.1.1"}
            )
            
            # Проверяем статус код
            assert response.status_code == 201
            
            # Проверяем, что функции были вызваны
            mock_giga.assert_called_once_with(test_prompt)
            mock_add.assert_called_once()



async def test_create_my_request_with_unknown_ip(ac: AsyncClient):
    # Тест для случая, когда request.client равен None и нет заголовка X-Forwarded-For
    test_prompt = "Тестовый запрос"
    test_response = "Тестовый ответ"
    
    # Мокаем функцию get_giga_response
    with patch('src.routers.requests.get_giga_response') as mock_giga:
        mock_giga.return_value = iter([['a', 'b', 'c', test_response]])
        
        # Мокаем функцию add_request_data
        with patch('src.routers.requests.add_request_data') as mock_add:
            mock_add.return_value = None
            
            # Отправляем POST запрос
            response = await ac.post("/requests/", json={"prompt": test_prompt})
            
            # Проверяем статус код
            assert response.status_code == 201
            
            # Проверяем, что функции были вызваны
            mock_giga.assert_called_once_with(test_prompt)
            mock_add.assert_called_once()


# async def test_create_my_request_db_error(ac: AsyncClient):
#     # Тест для случая, когда происходит ошибка базы данных
#     test_prompt = "Тестовый запрос"
#     test_response = "Тестовый ответ"
    
#     # Мокаем функцию get_giga_response
#     with patch('src.routers.requests.get_giga_response') as mock_giga:
#         mock_giga.return_value = iter([['a', 'b', 'c', test_response]])
        
#         # Мокаем функцию add_request_data для имитации ошибки БД
#         with patch('src.routers.requests.add_request_data') as mock_add:
#             mock_add.side_effect = SQLAlchemyError("Ошибка базы данных")
            
#             # Отправляем POST запрос
#             response = await ac.post("/requests/", json={"prompt": test_prompt})
            
#             # Проверяем, что получили ошибку 500
#             assert response.status_code == 500



# async def test_create_my_request_validation_error(ac: AsyncClient):
#     # Тест для случая, когда данные не проходят валидацию
#     test_prompt = "Тестовый запрос"
#     test_response = "Тестовый ответ"
    
#     # Мокаем функцию get_giga_response
#     with patch('src.routers.requests.get_giga_response') as mock_giga:
#         mock_giga.return_value = iter([['a', 'b', 'c', test_response]])
        
#         # Мокаем функцию add_request_data для имитации ошибки валидации
#         with patch('src.routers.requests.add_request_data') as mock_add:
#             mock_add.side_effect = ValueError("Ошибка валидации")
            
#             # Отправляем POST запрос
#             response = await ac.post("/requests/", json={"prompt": test_prompt})
            
#             # Проверяем, что получили ошибку 500
#             assert response.status_code == 500



async def test_create_my_request_empty_prompt(ac: AsyncClient):
    # Тест для случая, когда передан пустой prompt
    response = await ac.post("/requests/", json={"prompt": ""})
    
    # Проверяем, что получили ошибку 422 (ошибка валидации)
    assert response.status_code == 422