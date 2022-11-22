FROM python:3.9-alpine
WORKDIR /stripe

ENV PYTHONDONTWRITEBYTECODE 1\
    PYTHONUNBUFFERED 1

COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

RUN chmod +x entrypoint.sh
ENTRYPOINT ["sh", "entrypoint.sh"]