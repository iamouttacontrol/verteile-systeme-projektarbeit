FROM python:3.9-slim-buster

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r /app/requirements.txt
#EXPOSE 9000/tcp

COPY ./Backend/Main/Server.py /app/Server.py

EXPOSE 9000

CMD ["python", "./Server.py"]
