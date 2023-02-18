FROM python:3.8

WORKDIR /PHPSupport-bot/

COPY ./ /PHPSupport-bot

RUN pip install -r requirements.txt

EXPOSE 8080/tcp

WORKDIR /PHPSupport-bot/bot

CMD ["python", "main.py"]
