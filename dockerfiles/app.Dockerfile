FROM python:3.12.7
WORKDIR /src
RUN pip install --upgrade pip
COPY ../app/requirements.txt /src
RUN pip install -r requirements.txt
COPY ../app/src/ /src/
ENV PYTHONPATH=/src
