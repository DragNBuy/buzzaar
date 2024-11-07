FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
	gcc \
	libpq-dev \
	build-essential \
	python3-dev \
	pipx \
	--no-install-recommends && rm -rf /var/lib/apt/lists/*

COPY ./buzzaar_core/pyproject.toml .
RUN pipx ensurepath && . ~/.bashrc && pipx install poetry && poetry lock --no-update && poetry install

COPY . .

EXPOSE 8000

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
