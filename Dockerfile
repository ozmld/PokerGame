FROM alpine:latest

RUN apk add py3-pip

COPY . .

RUN pip3 install -r ./requirements.txt

CMD python3 ./PokerBot/main.py



