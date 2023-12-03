FROM python:3.9.18-slim-bullseye
COPY . /app
WORKDIR /app
ENV SIZE_LIMIT=100 INPUT_PATH=/input OUTPUT_PATH=/output
RUN pip install -r requirements.txt
ENTRYPOINT ["python","main.py"]