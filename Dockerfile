FROM python:3.12-slim

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY . ./

EXPOSE 5000

CMD ["uvicorn", "repo_monitor.main:app", "--host", "0.0.0.0", "--port", "5000"]
