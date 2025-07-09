# FASTESTING

## BASE FASTAPI PARA TESTEO

## TUTORIAL 
```
$ https://www.youtube.com/playlist?list=PLHftsZss8mw7pSRpCyd-TM4Mu43XdyB3R
```

### INSTALACION

1.- Primero debes instalar el entorno virtual utilizando :

```
$ pip install virtualenv
```

2.- Ahora debes crear el entorno virtual con:

```
$ python -m venv venv
```

3.- Posteriormente debes activar el entorno virtual utilizando:

```
$ source venv/scripts/activate
```

4.- Para finalizar la instalación debes utilizar:

```
$ pip install -r requirements.txt
```

### EJECUCION

1.- Para ejecutar la aplicacion debes utilizar :

```
$ uvicorn src.main:app --host=0.0.0.0 --port=5151 --reload
```

### VISUALIZACION

1.- Para visualizar la API podemos acceder al siguiente enlace:

```
http://localhost:5151/
```

2.- Si tu objetivo es revisar la documentación y testear los endpoints puedes visitar el siguiente enlace:

```
http://localhost:5151/docs
```