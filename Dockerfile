FROM python:3.9.2

RUN mkdir /app
WORKDIR /app

ADD main.py /app/main.py
ADD requirements.txt /app/requirements.txt
ADD server_pb2.py /app/server_pb2.py
ADD server_pb2_grpc.py /app/server_pb2_grpc.py

RUN pip install -r requirements.txt

ENTRYPOINT ['python', 'main.py']