FROM tiangolo/uvicorn-gunicorn:python3.11

RUN apt-get -y update
RUN apt-get install -y ffmpeg

WORKDIR /app

RUN pip install poetry
COPY poetry.lock pyproject.toml ./
RUN poetry install --without dev

COPY . .

CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]