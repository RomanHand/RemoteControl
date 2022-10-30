FROM python:3.10
LABEL maintainer="roma25r@gmail.com"

WORKDIR /rcserver
ADD . /rcserver
RUN pip install --upgrade pip && pip install wakeonlan && pip install pyyaml && pip install requests
EXPOSE 7890
CMD python3 server.py
