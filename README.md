# War in Hex - v0.4.0

Free implementation of a Hive style game without any copyright code/images. Also comes with two servers in Erlang and Python.

![Screenshot of War in Hex](Screenshot.png?raw=true "War in Hex in action")

```
├── assets					Assets
│   ├── black_boat_tile.png
│   ├── black_general_tile.png
│   ├── black_helicopter_tile.png
│   ├── black_tank_tile.png
│   ├── black_troops_tile.png
│   ├── playarea.png
│   ├── sideboard.png
│   ├── tile_drop.wav
│   ├── tiles.xcf
│   ├── white_boat_tile.png
│   ├── white_general_tile.png
│   ├── white_helicopter_tile.png
│   ├── white_tank_tile.png
│   └── white_troops_tile.png
├── game.py
├── main.py				Python script
├── main.exe				Windows binary (XP or later)
├── README.md
├── Screenshot.png
└── tile.py
```

### Running

Unix like systems

```
./main.py
```

On windows

```
./main.exe
```

The main.exe binary works for Windows versions XP and later, for 95 and 98 you can run setup.py to generate the required extra binary.

There are command line arguments for network support.

```
-n --network HOST:PORT  Enable network support.
-s --server    Act as server
```

To run a server on port 50006

```
$ ./main --network 0.0.0.0:50006 --server
```

or even

```
$ ./main -n :50005 -s
```

To connect a client to an already running server on localhost:50006

```
$ ./main --network localhost:50006
```

Or even

```
$ ./main -n :50006
```

### Online multiplayer

There are two server implementations currently, both allow random players to play against each other online.

The first is in erlang and started as so:

```
$ erl -noshell -s wihd start
```

And the second is in Python

```
$ python server.py
```

Now people can connect on :1664

And you will get to play with an available player. Very much alpha but if you organise it with someone perhaps it's possible?

### Dependencies

* python 2.7
* pygame

On Debian systems you may run

```
$ sudo apt-get install python-pygame
```

On windows install x86 python 2.7 (must be 32bit because of pygame) and pygame for python 2.7. If you wish to compile a binary for windows install py2exe.

### ToDo

* Debug + Error handling
* Make a server for online multiplayer
