#TODO: Search if there is a better image
FROM ubuntu

COPY ./src /code
COPY requirements.txt /code/config/requirements.txt
COPY gunicorn-config.py /code/config/gunicorn-config.py

RUN apt-get update
RUN apt-get install -y \
	python \
	python-pip \
	gunicorn

RUN pip install -r /code/config/requirements.txt

EXPOSE 5000

CMD ["/usr/bin/gunicorn", "--config", "/code/config/gunicorn-config.py", "wsgi:app"]	