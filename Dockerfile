FROM python:3.9.18-slim-bullseye
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
ENV SIZE_LIMIT=100 INPUT_PATH=/input OUTPUT_PATH=/output
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ["python","main.py"]