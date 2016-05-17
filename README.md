# Jupyter Notebook With Working Alignment Softwares

## Must do

* Be careful, the project directory have to be in ~/... (/home/...)
* You have to be in the "jupyter_align" project directory to run the following commands

## Build
```bash
$ docker build -t "pa/align" .
```

## Run
```bash
$ docker run -v ~/pa-inphinity/jupyter_align/src:/home/pa/work/jupyter_align -i -t -d -p 8888:8888 pa/align
```
