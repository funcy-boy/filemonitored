FROM python:3.7-alpine
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/
CMD [ "python3","manage.py","runserver","0:80" ]