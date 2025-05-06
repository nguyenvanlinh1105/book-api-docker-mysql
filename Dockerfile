FROM python:3.11-slim

WORKDIR /api

COPY ./build_api /api

RUN pip install fastapi uvicorn mysql-connector-python pandas

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
