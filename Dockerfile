#TODO: Search if there is a better image
FROM python:2.7

WORKDIR /usr/app

RUN python -m pip install --upgrade pip

RUN pip install --upgrade setuptools
RUN pip install gunicorn --install-option="--install-scripts=$PWD/bin"

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . . 

EXPOSE 5000

CMD ["./bin/gunicorn", "--config", "gunicorn-config.py", "wsgi:app"]	