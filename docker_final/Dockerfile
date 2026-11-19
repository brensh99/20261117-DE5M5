
FROM python:3.12-slim

WORKDIR /app

RUN pip install pandas

COPY eda_customers.py .
COPY "03_Library_SystemCustomers.csv" .

ENTRYPOINT ["python", "eda_customers.py"]
