FROM python:3.13

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["pytest"]
CMD ["app/tests/app_test.py", "-s"]