FROM python:3.8-alpine

# RUN apk add --update ffmpeg
RUN apk add ffmpeg

WORKDIR /app
COPY . /app


RUN python -m pip install -r requirements.txt

EXPOSE 5000

ENTRYPOINT ["python", "/app/srs/app.py"] 

# CMD ["/app/srs/app.py"]
