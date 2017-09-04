#TODO: Search if there is a better image
FROM python:2.7

COPY ./src /code
COPY requirements.txt /code/config/requirements.txt
COPY gunicorn-config.py /code/config/gunicorn-config.py

RUN python -m pip install --upgrade pip

RUN pip install --upgrade setuptools
RUN pip install gunicorn --install-option="--install-scripts=$PWD/bin"
RUN pip install -r /code/config/requirements.txt

EXPOSE 5000

CMD ["/bin/gunicorn", "--config", "/code/config/gunicorn-config.py", "wsgi:app"]	