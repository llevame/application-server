[![Build Status](https://travis-ci.org/llevame/application-server.svg?branch=master)](https://travis-ci.org/llevame/application-server) [![codecov](https://codecov.io/gh/llevame/application-server/branch/master/graph/badge.svg)](https://codecov.io/gh/llevame/application-server)

# application-server

Application Server para la aplicación Llevame

Desarrollado en **Python**, con **Flask** como framework back-end y **Gunicorn**.

### Correr Servidor

#### Dependencias

Se debe tener instalado [Docker CE](https://store.docker.com/search?offering=community&type=edition) 

En caso de exitir un error de permisos al ejecutar Docker, agregar al usuario al grupo para darle permisos:
```bash
$ sudo addgroup --system docker
$ sudo adduser $USER docker
$ newgrp docker
```

#### Ejecución

Primero se creara la imagen *appserver*, y luego se crea el container con el comando _run_
```bash
$ docker build -t appserver application-server/
$ docker run appserver
```

Para poder configurar el IP address, se debe crear un bridge con el container anter de ejecutarlo:
```bash
$ docker network create --driver=bridge --subnet=192.168.0.0/24 --gateway=192.168.0.1 mynet
$ docker run --net mynet --ip=192.168.0.10 appserver
```

Para corroborar se puede acceder a *192.168.0.10/5000* y ver la salida _Homepage_

#### Tests y Coverage

TODO: Update

```bash
(venv) $ pytest --cov-config .coveragerc --cov=$(pwd)
```
