FROM python:3.8-alpine
ADD . /app
WORKDIR /app
RUN apk update
RUN apk add python3-dev libffi-dev gcc musl-dev openssl-dev
RUN pip3 install -r requirements.txt
CMD ["python", "app.py"]
