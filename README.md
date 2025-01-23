# ossas-MusicPlayer

![screenshot](image.png)

## how to install

```bash
git clone github.com/j03-dev/osas-player
cd osas-player
python -m pip install -r requirements.txt
```

## config

_open_ **.config** and change<br>

```
path = your music directory
```

## To run this project
you need to build osas lib , for that u need rust installed
before , i use pygame mixer to play music, so i decide to use **rodio** lib from **rust** and use **py03**
to create lib from rust -> python

```bash
cd osas
maturin develop
```
Then you can run the application
```
python main.py
```
