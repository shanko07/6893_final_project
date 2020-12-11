FROM python:rc-alpine

COPY app.py .

RUN pip install requests flask

ENTRYPOINT [ "python" ]

CMD [ "app.py" ]
