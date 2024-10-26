FROM python:3.12.7
WORKDIR /src
RUN pip install --upgrade pip
COPY ../app/requirements.txt /src
RUN pip install -r requirements.txt
COPY ../.venv/Lib/site-packages/ /usr/local/lib/python3.12/site-packages/
#RUN pip install -r requirements.txt --find-links /usr/local/lib/python3.12/site-packages
COPY ../app/src/ /src/
ENV PYTHONPATH=/src
