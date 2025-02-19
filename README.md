# FastAPI_wav2mp3
Простой сервис для конвертации wav в mp3 (тестовое задание)


### Технологии
 - Backend: FastAPI (Python)

 - База данных: PostgreSQL

 - ORM: SQLAlchemy

 - Контейнеризация: Docker, Docker Compose

### Требования
- Установленные Docker и Docker Compose. 
- Порт 8000 должен быть свободен (для работы сервиса).
- make для запуска через Makefile

### Запуск проекта

1. Клонируйте репозиторий:
```bash
git clone <ваш-репозиторий>
cd <папка-проекта>
```
2. Запустите сервис через Makefile:
```bash
make run
```


3. Остановка контейнеров:


```bash
make down
```

### Использование API
#### 1. Создание пользователя
(С помощью curl или в интерактивной документации по ссылке http://localhost:8000/docs)
#### Запрос:


```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/users' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "alexander"
}'
```
#### Ответ:

```json
{
  "id": "c94df9e1-8c15-482c-bcac-322db78cf6b8",
  "token": "e97b3f47-2eee-40c0-bcea-4c9b1da5b2ea"
}
```
#### 2. Конвертация аудиозаписи

#### Запрос:

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/record?user_id=c94df9e1-8c15-482c-bcac-322db78cf6b8&token=e97b3f47-2eee-40c0-bcea-4c9b1da5b2ea' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'wav_file=@some_audio.wav;type=audio/wav'
  ```
#### Ответ:

```json
{
  "download_link": "http://localhost:8000/record?id=ab5e879a-1dda-4296-91a5-4f889f4f8e02&user_id=c94df9e1-8c15-482c-bcac-322db78cf6b8"
}
```
#### 3. Скачивание аудиозаписи

Перейдите по ссылке из ответа метода конвертации:

```bash
curl -X GET "http://localhost:8000/record?id=<record_id>&user=<user_id>"
```
### Особенности реализации
 - Хранение данных:
    - Аудиофайлы сохраняются в папках по user_id (например, app/media/<user_id>/<record_id>.mp3).

    - При повторной загрузке файла с тем же именем возвращается ошибка 409 Conflict.

 
 - Volumes:

    - Данные PostgreSQL хранятся в db_volume.

    - Аудиофайлы сохраняются в media.