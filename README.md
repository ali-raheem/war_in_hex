# War in Hex - v0.3.2

Free implementation of a Hive style game without any copyright code/images.

![Screenshot of War in Hex](Screenshot.png?raw=true "War in Hex in action")

├── assets
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
├── main.py
├── README.md
├── Screenshot.png
└── tile.py


### Running

Unix like systems

```
./main.py
```

Network features are very buggy.

```
--network   Enable network support.
--server    Act as server
```

To run a server on port 50006

```
$ ./main --network 0.0.0.0:50006 --server
```

To connect a client to an already running server on localhost:50006

```
$ ./main --network localhost:50006
```

### Dependencies

* python 2.7
* pygame

On Debian systems you may run

```
$sudo apt-get install python-pygame
```

### ToDo

* Debug network and add in error handling
