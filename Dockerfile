FROM python:3.10-alpine3.14

WORKDIR /api

ENV PORT=8000
ENV DB=entities.json

COPY requirements.txt .
COPY assignment .

RUN pip install -r requirements.txt

EXPOSE 8000
CMD ["python", "app.py"]