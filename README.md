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

Primero se creará la imagen *appserver*
```bash
$ docker build -t appserver application-server/
```

Luego se crea (y ejecuta) el container *AppServer*. Para poder configurar el IP address, 
se debe crear un bridge con el container anter de ejecutarlo:
```bash
$ docker network create --driver=bridge --subnet=192.168.0.0/24 --gateway=192.168.0.1 mynet
$ docker run --net mynet --ip=192.168.0.10 --name AppServer appserver
```

Para corroborar que este corriendo, se puede acceder a *192.168.0.10/5000* y ver la salida _Homepage_

A partir de este punto ya está creado el container AppServer, con la ip asociada. En caso de cerrarlo, 
puede reiniciarse con el comando _start_
```bash
$ docker start AppServer
```

#### Tests

```bash
docker exec AppServer pytest
```
