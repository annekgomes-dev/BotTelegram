FROM python:3.10

WORKDIR /app

COPY app/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY app .

CMD ["python", "main.py"]
