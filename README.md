# KazanExpress

## Как запустить проект?

Клонируйте репозиторий
```
git clone git@github.com:kurrbanov/kazanexpress-admin.git
```

Переименуйте переменные окружения и файл в ```.env```
```
cp .env.examle .env
```

Запустите проект через docker-compose
```
docker-compose up -d --build
```