FROM python:3.8.12-slim

WORKDIR .

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

EXPOSE 5005

COPY . .
CMD ["python", "service.py"]