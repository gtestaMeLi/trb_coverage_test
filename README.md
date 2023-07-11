# trb_coverage_test

brew install postgresql@14
pgAdmin4 -> https://www.pgadmin.org/download/

pip install -r requirements.txt

se crea un servidor y un schema en postgres, y creamos un .env:

```
DATABASE_NAME=db_name
DATABASE_USER=db_user
DATABASE_PASS=db_user_pass
```

Para instalar postgis, abrir el servidor en pgAdmin4, ir a la sección "Extensions", click derecho -> Create -> Extension, buscar `postgis` e instalar. 