FROM python:3.10-slim

WORKDIR /app

COPY . .

ENV AWS_ACCESS_KEY_ID=""
ENV AWS_SECRET_ACCESS_KEY=""
ENV BUCKET_NAME=""
ENV URL=""

RUN pip install -r requirement.txt

CMD ["python", "app.py"]

