FROM python:3.12-slim

ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

COPY entrypoint.sh .
RUN sed -i 's/\r$//g' /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

EXPOSE 8000
CMD ["gunicorn", "run:app", "--bind", "0.0.0.0:8000", "--timeout", "3600", "--workers", "4"]
