FROM python:3.10-alpine
MAINTAINER YanLi
ENV FLASK_APP="wsgi.py"
ENV SELENIUM_URL="http://selenium:4444/wd/hub"
COPY . /app
WORKDIR /app
RUN pip3 install -r requirements.txt