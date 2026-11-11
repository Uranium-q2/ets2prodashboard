FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .
COPY templates/ templates/

EXPOSE 5000

ENV ETS2_API_URL=http://host.docker.internal:25555/api/ets2/telemetry

CMD ["python", "main.py"]
