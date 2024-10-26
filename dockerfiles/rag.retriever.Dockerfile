FROM python:3.12.7
LABEL authors="pomelk1n"


ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache \
    PYTHONPATH=/app

RUN groupadd -r user && useradd -r -g user user && \
  curl -sSL https://install.python-poetry.org | python3 - && \

RUN mkdir -p /home/user/.cache/huggingface \
    && chown -R user:user /home/user/.cache/huggingface

COPY --chown=user:user . /app

WORKDIR /app

RUN poetry install --without dev --no-root && rm -rf $POETRY_CACHE_DIR

ENTRYPOINT ["poetry", "run", "uvicorn", "retriever.main:app", "--host", "0.0.0.0", "--port", "8000"]