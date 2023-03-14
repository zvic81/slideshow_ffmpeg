FROM python:alpine3.16

RUN apk add --update ffmpeg && rm -rf /var/lib/apt/lists/* 

WORKDIR /app
COPY . /app

# RUN python -m pip install --upgrade pip && 
RUN python -m pip install -r requirements.txt

EXPOSE 5000

ENTRYPOINT ["python", "/app/srs/app.py"] 


