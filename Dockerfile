FROM python:3.8-slim-buster

RUN mkdir /app

WORKDIR /app

COPY requirements.txt . 

RUN pip install -r requirements.txt

COPY . . 
EXPOSE 8989

CMD ["uvicorn", "main:app", "--host=0.0.0.0", "--port=8989"]

