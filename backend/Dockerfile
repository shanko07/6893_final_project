FROM ubuntu:latest

RUN apt update && apt install -y python3 python3-pip

COPY app.py .

RUN python3 -m pip install requests flask joblib pandas sklearn

ENTRYPOINT [ "python3" ]

CMD [ "app.py" ]
