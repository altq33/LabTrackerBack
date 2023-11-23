# Fast API Project

Этот проект создан с использованием FastAPI, Alembic для управления миграциями базы данных, и Poetry для управления зависимостями Python.

## Установка

1. Клонируйте репозиторий:

   
   git clone https://github.com/altq33/LabTrackerBack.git
   

2. Перейдите в директорию проекта:

   
   cd fastapi-project
   

3. Установите зависимости проекта с помощью Poetry (если Poetry еще не установлен) или через requerments.txt:

   
   poetry install
   

## Применение миграций базы данных

Для применения миграций базы данных используйте следующую команду:

alembic upgrade head


Это применит все доступные миграции к базе данных.

## Запуск сервера

Для запуска FastAPI сервера используйте следующую команду:

uvicorn app.main:app --reload


После выполнения этой команды, сервер должен запуститься и стать доступным по адресу http://localhost:8000.

## Вклад

Если вы хотите внести вклад в этот проект, не стесняйтесь отправлять pull request или открывать issue.

## Лицензия

Этот проект лицензирован в соответствии с условиями лицензии MIT - подробности см. в файле LICENSE.
