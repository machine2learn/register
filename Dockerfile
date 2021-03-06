FROM python:3.6.8-alpine3.8 

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev
RUN apk add git
RUN git clone https://github.com/machine2learn/register.git
WORKDIR /register
RUN pip install -r requirements.txt
ENTRYPOINT ["python", "main.py"]
