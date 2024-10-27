FROM python:3.12.7
LABEL authors="pomelk1n"

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache \
    PYTHONPATH=/app

# Install curl and create a user
RUN apt-get update && apt-get install -y curl && \
    groupadd -r user && useradd -r -g user user && \
    curl -sSL https://install.python-poetry.org | python3 -

# Create necessary directories and set permissions
RUN mkdir -p /home/user/.cache/huggingface && \
    chown -R user:user /home/user/.cache/huggingface

# Set the working directory and copy the application code
COPY --chown=user:user . /app/retriever
WORKDIR /app/retriever

# Install dependencies with Poetry
RUN poetry install --without dev --no-root && rm -rf $POETRY_CACHE_DIR

# Set entrypoint for running the application
ENTRYPOINT ["poetry", "run", "uvicorn", "retriever.main:app", "--host", "0.0.0.0", "--port", "8000"]
