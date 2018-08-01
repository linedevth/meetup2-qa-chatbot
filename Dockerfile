FROM python:alpine3.6

RUN apk add --update curl gcc g++ \
    && rm -rf /var/cache/apk/*
RUN ln -s /usr/include/locale.h /usr/include/xlocale.h

WORKDIR /app
ADD ./requirements.txt /app
ADD * /app/

RUN pip install -r ./requirements.txt

CMD ["python", "./app.py"]

EXPOSE 6000