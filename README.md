# Jupyter Notebook for MLBD project

## Must do

* Be careful, the project directory have to be in ~/... (/home/...)


## Build
```bash
$ docker build -t "mlbd/jupyter" .
```

## Run
```bash
$ docker run -v ~/jupyter_mlbd/src:/home/pa/work/ -i -t -d -p 8889:8888 mlbd/jupyter
```
