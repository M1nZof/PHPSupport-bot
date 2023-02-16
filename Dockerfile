FROM python:3.8

WORKDIR .

# COPY . /bot

RUN pip install -r requirements.txt

EXPOSE 8080/tcp

CMD ["python", "main.py"]
