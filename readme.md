🚀 Team Finder

📋 Описание
Краткое описание проекта: веб-приложение на Django для поиска и создания команд, фильтрации проектов по навыкам и управления участниками.

🛠️ Технологии
Backend: Python 3.13, Django 5.2, PostgreSQL 16

Контейнеризация: Docker, Docker Compose

Frontend: HTML, CSS, JavaScript (Pillow для генерации аватаров)

🚦 Быстрый старт
Предварительные требования
Установленные Docker и Docker Compose (входят в Docker Desktop).

Git (для клонирования репозитория).

1. Клонирование репозитория
bash
git clone https://github.com/kostya019/team-finder-ad.git
cd team-finder
2. Настройка переменных окружения
Скопируйте файл-образец .env_example в .env:

bash
cp .env_example .env
Откройте .env в любом текстовом редакторе и укажите корректные значения для вашего окружения.

📌 Переменные окружения
Переменная	Назначение
DJANGO_SECRET_KEY	Секретный ключ Django. Можно сгенерировать командой python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
DJANGO_DEBUG	Режим отладки. Для разработки установите True, для продакшена – False.
POSTGRES_DB	Имя базы данных PostgreSQL.
POSTGRES_USER	Имя пользователя БД.
POSTGRES_PASSWORD	Пароль пользователя БД.
POSTGRES_HOST	Хост БД. При локальном запуске через Docker укажите db (имя сервиса в compose).
POSTGRES_PORT	Порт БД (по умолчанию 5432).
TASK_VERSION	Номер варианта задания (используется для выбора набора шаблонов). В данном варианте - 3.
3. Запуск приложения
Выполните в корневой папке проекта:

bash
docker-compose up -d
Флаг -d запускает контейнеры в фоновом режиме.
При первом запуске будут автоматически собраны образы, созданы и запущены контейнеры db, backend и gateway (nginx).

4. Проверка работы
После успешного запуска откройте браузер и перейдите по адресу: http://localhost (или http://localhost:8000, если не используете nginx).

Вы должны увидеть страницу со списком проектов.

5. Применение миграций (если не выполнены автоматически)
Иногда миграции не применяются автоматически из-за порядка запуска. В таком случае выполните вручную:

bash
docker-compose exec backend python manage.py migrate
6. Создание суперпользователя (для доступа в админку)
bash
docker-compose exec backend python manage.py createsuperuser
Админка доступна по адресу http://localhost/admin.

🛑 Остановка и удаление контейнеров
Остановка (контейнеры останавливаются, но не удаляются):

bash
docker-compose down

Остановка + удаление томов (будут потеряны все данные в БД, статика и медиа):

bash
docker-compose down -v

📦 Полезные команды
Просмотр логов всех сервисов:

bash
docker-compose logs -f
Просмотр логов конкретного сервиса (backend / db / gateway):

bash
docker-compose logs -f backend
Пересборка образов и запуск:

bash
docker-compose up --build -d
Вход в контейнер backend:

bash
docker-compose exec backend bash
Выполнение произвольной команды Django (например, сбор статики):

bash
docker-compose exec backend python manage.py collectstatic --noinput
📁 Структура проекта (кратко)
text
.
├── backend/                # Django приложение
│   ├── Dockerfile
│   ├── manage.py
│   ├── requirements.txt
│   ├── team_finder/        # основной проект Django
│   ├── users/              # приложение пользователей
│   ├── projects/           # приложение проектов
│   └── ...
├── nginx/                   # конфигурация Nginx
│   ├── Dockerfile
│   └── default.conf
├── docker-compose.yml
├── .env_example
└── README.md               # этот файл

✨ Авторы
@KhelinKonstantin
