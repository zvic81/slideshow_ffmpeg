FROM python:3.8-alpine

RUN apk add --update ffmpeg

WORKDIR /app
COPY . /app


RUN python -m pip install -r requirements.txt

EXPOSE 5000

ENTRYPOINT ["python"]

CMD ["/app/srs/app.py"]