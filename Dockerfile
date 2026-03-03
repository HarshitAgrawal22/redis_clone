# official slim python image
FROM python:3.12-slim

WORKDIR /app
# Prevent Python from writing pyc files
ENV PYTHONDONTWRITEBYTECODE=1
# Ensure output is printed immediately
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app
COPY req.txt req.txt

RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r req.txt

COPY . .
EXPOSE 6001 
EXPOSE 5001
RUN ls -R /app/python_redis
CMD ["python" , "-m" , "python_redis.main"]
