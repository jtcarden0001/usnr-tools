FROM python:3.13

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

RUN ls -al
RUN echo $PW
COPY . .
RUN pytest tests/