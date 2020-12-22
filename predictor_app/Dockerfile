FROM ubuntu:latest

RUN apt update && apt install -y python3 python3-pip

RUN python3 -m pip install requests flask

COPY . .

ENTRYPOINT [ "python3" ]

CMD [ "app.py" ]
