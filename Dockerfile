FROM python:3.8

RUN apt-get update -y

WORKDIR /var/task

COPY lambda_requirements.txt .

RUN pip install --upgrade pip &&\
    pip install -r lambda_requirements.txt -t /layer/python/lib/python3.8/site-packages/

CMD ["bash"]
