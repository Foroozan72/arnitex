FROM python:3.9
ENV PYTHONUNBUFFERED=1
WORKDIR /django
COPY . .
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt


COPY ./entrypoint.sh /
ENTRYPOINT ["sh", "/entrypoint.sh"]