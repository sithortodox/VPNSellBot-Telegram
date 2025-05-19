# VPNSellBot Telegram

**VPNSellBot** — асинхронный Telegram-бот на базе `aiogram` для автоматизации продажи VPN-доступа. Поддерживает пользовательские и админские команды, хранит данные в PostgreSQL, защищён от спама и легко разворачивается через Docker.

---

## Возможности

- Регистрация и приветственное сообщение (`/start`)  
- Просмотр баланса и пополнение (пользовательский раздел)  
- Личный кабинет: история платежей, активных подписок (`/cabinet`)  
- Админ-панель: массовые рассылки, управление балансом пользователей, статистика  
- Антифлуд-middlewares с настраиваемым интервалом  
- Пагинация для вывода длинных списков (история, статистика)  
- Логирование через `logging.config`  
- Полностью асинхронная работа с БД через SQLAlchemy + asyncpg  

---

## Быстрый старт

1. Клонировать репозиторий и перейти в папку:
    ```bash
    git clone https://github.com/sithortodox/VPNSellBot-Telegram.git
    cd VPNSellBot-Telegram
    ```

2. Скопировать шаблон настроек и заполнить значения:
    ```bash
    cp .env.example .env
    # Открыть .env и указать:
    # TELEGRAM_BOT_TOKEN
    # DATABASE_URL
    # LOG_LEVEL и т.д.
    ```

3. Собрать и запустить через Docker Compose:
    ```bash
    docker-compose up -d --build
    ```

4. Проверить логи бота:
    ```bash
    docker-compose logs -f bot
    ```

---

## Локальная разработка

1. Создать и активировать виртуальное окружение:
    ```bash
    python3.11 -m venv .venv
    source .venv/bin/activate
    ```

2. Установить зависимости:
    ```bash
    pip install -r requirements.txt
    ```

3. Запустить PostgreSQL локально (или через Docker), настроить `DATABASE_URL` в `.env`.

4. Запустить бота:
    ```bash
    export $(grep -v '^#' .env | xargs)
    python -m vpnsellbot.main
    ```

---

## Переменные окружения

Все необходимые переменные описаны в файле `.env.example`:

```dotenv
TELEGRAM_BOT_TOKEN=ваш_токен
DATABASE_URL=postgresql+asyncpg://user:pass@localhost:5432/vpnsell
LOG_LEVEL=INFO
THROTTLE_RATE=1.0
ADMIN_IDS=123456789,987654321
DEFAULT_PAGE_SIZE=10


vpnsellbot/
├── main.py              — точка входа, инициализация бота и роутеров
├── config.py            — загрузка настроек из .env
├── logging_config.py    — настройка логгера
├── db/
│   ├── dao.py           — функции CRUD для работы с БД
│   └── models.py        — модели SQLAlchemy
├── handlers/
│   ├── admin/           — админ-роутеры (рассылки, статистика, пополнение)
│   └── user/            — пользовательские роутеры (/start, /balance, /cabinet)
├── keyboards/
│   └── user_kb.py       — инлайн-клавиатуры и callback data
├── middlewares/
│   └── throttling.py    — антифлуд middleware
└── utils/
    └── pagination.py    — утилиты для пагинации

Дополнительно в корне:

.env.example — пример файла окружения

Dockerfile, docker-compose.yml — для контейнеризации

scripts/replace_ellipses.py — утилита для замены ... на NotImplementedError

tests/ — модульные тесты

Contributing
Форкните репозиторий

Создайте ветку feature/ваша-фича или fix/исправление

Напишите код и тесты

Откройте Pull Request с описанием изменений

Перед коммитом запускайте:

pre-commit run --all-files
pytest
