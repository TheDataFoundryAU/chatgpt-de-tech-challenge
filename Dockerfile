FROM python:3.8

RUN apt-get update -y

WORKDIR /var/task

COPY requirements.txt .

RUN pip install --upgrade pip &&\
    pip install -r requirements.txt -t /python/lib/python3.8/site-packages/

CMD ["bash"]
