FROM python:3.9

WORKDIR /src
COPY dev.txt /src
RUN pip3 install --upgrade pip -r dev.txt

COPY . /src

EXPOSE 5000
