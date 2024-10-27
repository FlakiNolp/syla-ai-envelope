FROM python:3.12.7
WORKDIR /src
RUN pip install --upgrade pip
COPY ../auth/pyproject.toml /src
RUN pip install .
COPY ../auth/src/ /src/
ENV PYTHONPATH=/src
