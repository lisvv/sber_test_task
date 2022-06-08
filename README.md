[![Sber Task CI](https://github.com/lisvv/sber_test_task/actions/workflows/actions.yml/badge.svg)](https://github.com/lisvv/sber_test_task/actions/workflows/actions.yml)

Тестовое задание Sber

### Порядок запуска проекта:

1. Колонируем репозиторий: 
```git clone https://github.com/lisvv/sber_test_task.git```

2. Переходим в пап 

3. Переименовываем файл с переменными окружения
```mv .env.example .env```

4. Переходим в папку cats_infra
```cd cats_infra```

5. Запускаем проект
```docker-compose up -d```

После запуска проект будет доступен локально по адресу:
http://localhost:8000/

Также есть возможность посмотреть развернутый проект на сервере:

### Краткое описание проекта

Проект Представляет собой API для магазина котят с админкой и документацией к API с использованием Swagger
Также в проекте реализован пайплайн который проверяет функционирование CRUD и после чего создает docker-образ
и пушит его в YandexRegistry.
