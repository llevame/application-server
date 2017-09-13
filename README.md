[![Build Status](https://travis-ci.org/llevame/application-server.svg?branch=master)](https://travis-ci.org/llevame/application-server) [![codecov](https://codecov.io/gh/llevame/application-server/branch/master/graph/badge.svg)](https://codecov.io/gh/llevame/application-server)

# application-server

Application Server para la aplicación Llevame

Desarrollado en **Python**, con **Flask** como framework back-end y **Gunicorn**.

## Correr Servidor

Se recomienda el uso de Docker para evitar las diferencias que pudiera haber al instalar el ambiente.

### Dependencias

#### Docker
Se debe tener instalado [Docker CE](https://store.docker.com/search?offering=community&type=edition) 

En caso de existir un error de permisos al ejecutar Docker, agregar al usuario al grupo para darle permisos:
```bash
$ sudo addgroup --system docker
$ sudo adduser $USER docker
$ newgrp docker
```

#### Local - Configuración del ambiente de desarrollo
Se necesitan *python*, *pip*, y en particular *virtualenv*.
```bash
$ sudo pip install virtualenv
```

### Ejecución

#### Docker
Primero se creará la imagen *appserver*
```bash
$ docker build -t appserver application-server/
```

Luego se crea (y ejecuta) el container *AppServer*. Para poder configurar el IP address, 
se debe crear un bridge con el container antes de ejecutarlo:
```bash
$ docker network create --driver=bridge --subnet=192.168.0.0/24 --gateway=192.168.0.1 mynet
$ docker run --net mynet --ip=192.168.0.10 --name AppServer appserver
```

Para corroborar que este corriendo, se puede acceder a *192.168.0.10:5000* y ver la salida _Homepage_

A partir de este punto ya está creado el container AppServer, con la ip asociada. En caso de cerrarlo, 
puede reiniciarse con el comando _start_
```bash
$ docker start AppServer
```

#### Local - Ejecución en el ambiente de desarrollo
Levantar la VM donde correrá el servidor
```bash
$ virutalenv venv
```
+ Evitar pushear el archivo generado a partir de la anterior ejecución (si se usa **venv** este ya está agregado al .gitignore)
 
```bash
$ source venv/bin/activate
```
+ Se verá en el *promt* el nombre del directorio creado anteriormente entre paréntesis

Instalar los requerimientos en la VM 
```bash
(venv) $ pip install -r requirements.txt
```

Finalmente ejecutar *gunicorn*. Para corroborar se puede acceder a *localhost:5000* y ver la salida _Homepage_
```bash
(venv) $ gunicorn --bind localhost:5000 wsgi:app --chdir src/
```

### Tests

#### Docker
```bash
docker exec AppServer pytest
```

#### Local - Ejecución en el ambiente de desarrollo
```bash
(venv) $ pytest --cov-config .coveragerc --cov=$(pwd)
```
