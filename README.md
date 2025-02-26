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
git clone https://github.com/alexanderchainsaw/FastAPI_wav2mp3.git
cd FastAPI_wav2mp3
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
  'http://localhost:8000/record?user_id=c5975e47-fac0-4b61-876d-20d5e1c4cb3a' \
  -H 'accept: application/json' \
  -H 'token: e97b3f47-2eee-40c0-bcea-4c9b1da5b2ea' \
  -H 'Content-Type: multipart/form-data' \
  -F 'wav_file=@some_audio.wav;type=audio/wav'
  ```
#### Ответ:

```json
{
  "download_link": "http://localhost:8000/record?id=4b4afdbb-4807-42c4-ab97-3f192597e196&user_id=c5975e47-fac0-4b61-876d-20d5e1c4cb3a"
}
```
#### 3. Скачивание аудиозаписи

Отправить GET запрос по ссылке (в заголовке нужно указать токен):

```bash
curl -X 'GET' \
  'http://localhost:8000/record?id=4b4afdbb-4807-42c4-ab97-3f192597e196&user_id=c5975e47-fac0-4b61-876d-20d5e1c4cb3a' \
  -H 'accept: application/json' \
  -H 'token: e97b3f47-2eee-40c0-bcea-4c9b1da5b2ea'
```
### Особенности реализации

- Аудиофайлы сохраняются в папках по user_id (например, app/media/<user_id>/<название_файла>.mp3).

 - При повторной загрузке файла с тем же именем возвращается ошибка 409 Conflict.
  
 - Создание пользователя с существующим именем разрешено, так как идентификация происходит по id и кофликтов не возникает
 - Для создания и скачивания аудио пользователь должен предоставить свой token, который был выдан при регистрации

 
 - Volumes:

    - Данные PostgreSQL хранятся в db_volume.

    - Аудиофайлы сохраняются в media.
