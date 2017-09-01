[![Build Status](https://travis-ci.org/llevame/application-server.svg?branch=master)](https://travis-ci.org/llevame/application-server) [![codecov](https://codecov.io/gh/llevame/application-server/branch/master/graph/badge.svg)](https://codecov.io/gh/llevame/application-server)

# application-server

Application Server para la aplicación Llevame

Desarrollado en **Python**, con **Flask** como framework back-end y **Gunicorn**.

### Correr Servidor

#### Dependencias

Se necesitan *python*, *pip*, y en particular *virtualenv*.
Para descargarlo ejecutar:

> $ sudo pip install virtualenv


#### Ejecución

> $ virutalenv venv

- (usar este nombre que está agregado al .gitignore y no se subirá al realizar un *commit and push*)

> $ source venv/bin/activate

- (se verá en el *promt* que se agrega entre paréntesis el nombre del directorio creado anteriormente)

> (venv) $ pip install -r requirements.txt

> (venv) $ gunicorn --bind localhost:5000 wsgi:app -chdir src/

#### Tests y Coverage

> (venv) $ pytest --cov-config .coveragerc --cov=$(pwd)
