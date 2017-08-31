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

- (usar este nombre que está agregado al .gitignore y no  se subira al realizar un *commit and push*)

> $ source venv/bin/activate

- (se verá en el *promt* que se agrega entre paréntesis el nombre del directorio creado anteriormente)

> $ pip install -r requirements.txt

> $ gunicorn --bind localhost:5000 wsgi:app -chdir src/

#### Tests

> $ python src/test/tests.py
