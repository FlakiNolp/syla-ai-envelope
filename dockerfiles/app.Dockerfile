FROM python:3.12.7
WORKDIR /src
RUN pip install --upgrade pip
COPY ../app/pyproject.toml /src
RUN pip install .
COPY ../app/src/ /src/
ENV PYTHONPATH=/src
