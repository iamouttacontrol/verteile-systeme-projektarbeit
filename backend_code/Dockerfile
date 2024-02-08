FROM python:3.9-slim-buster

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r /app/requirements.txt
#EXPOSE 9000/tcp

COPY ./backend_code/server_2.py /app/server_2.py

#ENV FLASK_APP=server_2.py

EXPOSE 9000

CMD ["python", "./server_2.py"]
