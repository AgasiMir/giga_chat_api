from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routers import routers

app = FastAPI(title="AI стартап", version="1.0.0")


for router in routers:
    app.include_router(router)


# -----------------------------------------------------
# CORS нужен только в случае, если ваш FastAPI обслуживает запросы от фронтенда,
# который находится, например, на другом домене, порту. А если у вас публичное API,
# то и CORS не нужен.

# публичное апи - ставим allow_origins=[*] (для явности) или просто не указываем
# апи для фронта - ставим в allow_origins адрес/домен нашего фронта
# апи для серверов/приложух - ставим allow_origins=[] (потому что так лучше для zero trust)

# Настройки CORS
origins = [
    "http://localhost:3000",  # React/Vite dev server
    "http://127.0.0.1:3000",  # React/Vite dev server (альтернативный адрес)
    "http://localhost:5000",  # Live Server (VS Code)
    "http://127.0.0.1:5000",  # Live Server (альтернативный адрес)
    "http://localhost:5500",  # Live Server (WebStorm/другие IDE)
    "http://127.0.0.1:5500",  # Live Server (альтернативный адрес)
    # когда браузер делает запрос из локального файла (например, file://.../index.html),
    # то источник запроса должен быть указан как "null"
    "null",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# если в origins указать "null", то можно просто запустить
# index.html, без python -m http.server номер порта

# запустить FastAPI сервер, добавить новый терминал (или сделать сплит) и ввести:
# python -m http.server 3000
# или
# python -m http.server 5000

# Затем в адресную строку браузера ввести один из следующих адресов:
# http://localhost:3000/index.html
# http://localhost:5000/index.html
