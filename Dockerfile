FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11

WORKDIR /app

COPY . /app

RUN pip3 install -r requirements.txt

RUN pipwin install pyaudio

EXPOSE 8000

CMD ["python", "main.py"]