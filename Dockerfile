FROM python:3.11

WORKDIR /stat_guru_bot

COPY . .
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "run.py"]
