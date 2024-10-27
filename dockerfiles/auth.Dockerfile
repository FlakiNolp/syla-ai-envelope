FROM python:3.12.7
WORKDIR /src
RUN pip install --upgrade pip
COPY ../auth/requirements.txt /src
RUN pip install -r requirements.txt
COPY ../auth/src/ /src/
ENV PYTHONPATH=/src
