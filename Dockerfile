FROM python:3.8

RUN dir

WORKDIR ./bot

RUN dir

# COPY . /bot

RUN pip install -r requirements.txt

EXPOSE 8080/tcp

CMD ["python", "main.py"]
