FROM python:3.12

WORKDIR /backend

COPY ./requirements.txt ./requirements.txt

RUN pip install -r requirements.txt

COPY . .

CMD ["python3", "main.py"]