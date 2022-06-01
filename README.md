# Kalaha

![Game window](images/image-1.jpg)

## Installation
This game requires additional Python libraries. Install them using `pip` command.
```
pip install -r requirements.txt
```

## Using C++ extensions
To speed up best move search CMiniMax algorithm has been written in C++.
Build them by using following command.
```shell
python setup.py build
```
Read more about using C++ in Python code [here](https://docs.python.org/3/extending/extending.html).


## Running server

### From source

Use `server` argument to start the server. By running following command 
server will listen for connections on `127.0.0.1:20202` with turn timeout of `60` seconds.
```shell
python -m kalaha server -H 127.0.0.1 -p 20202 -tt 60
```
### Using Docker
Update environment variables in `docker-compose.yml` file and spin up containers.
```shell
docker-compose up
```

## Running client

### Human player

Start client and connect with server IP address and port autofilled.
```shell
python -m kalaha client -H 127.0.0.1 -p 20202
```

### Auto player

Auto player can be configured via in-game GUI or command arguments. __Note: You will not be able to make moves manually.__

Start client, connect to server and enable autoplay.
This command configures minimax algorithm to search for best move in tree of depth `4`.
Delay of auto move will be `5` seconds.
```shell
python -m kalaha client -ap -apd 5 -md 4
```
You can enable alpha-beta pruning by passing `-ab` argument.
```shell
python -m kalaha client -ap -apd 5 -md 4 -ab
```
You can enable iterative deepening by passing `-id` argument.
```shell
python -m kalaha client -ap -apd 5 -md 4 -id
```
To enable move highlighting, pass `-hm` argument.
```shell
python -m kalaha client -hm -md 4
```

## FAQ

### What game modes are available?
Human vs. Human, Human vs. Auto player, Auto player vs. Auto player.

### Is input validation done on the server side or client side?
Every move including pit selection is validated on the server side.

### How auto game works?
Autoplayer uses minimax algorithm to find the best move. Optimalizations were made to improve the performance
and win rate.
- iterative deepening
- alpha-beta pruning
- tree is generated level by level when minimax traverses the tree
- auto player is written in C++

__Important__: Algorithm is run on client side. It is running in separate thread, 
but setting high tree depth can cause the client to freeze and exceed the player's time limit.
Recommended tree depth is `4`.

### What Python libraries are used?
- qtpy - abstraction layer for PyQt5/PySide2
- PyQt5 - Qt5 bindings for Python
- [qrainbowstyle](https://github.com/desty2k/QRainbowStyleSheet) - custom windows and widgets style
- [QtPyNetwork](https://github.com/desty2k/QtPyNetwork) - high level network library
- coloredlogs - colored logging
