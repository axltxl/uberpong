Uber Pong!
==========

An *Uber-engineered* and somewhat overthought multiplayer implementation of a classic game.

![](http://i.imgur.com/gSYqI2q.jpg) ![](http://i.imgur.com/K5IpCPr.jpg)

**NOTE: Uber Pong! is currently on its first alpha state, meaning that everything
is subject to change!**

##Requirements
* [python](http://python.org) >= 3.3
* [pyglet](http://pyglet.org)
* [pymunk](http://pymunk.readthedocs.org)
* [docopt](http://docopt.org)
* [lz4](https://pypi.python.org/pypi/lz4)
* [simpleubjson](https://pypi.python.org/pypi/simpleubjson)
* [bson](https://pypi.python.org/pypi/bson)

## Features
* Painless installation
* Client-server paradigm, meaning it comes with multiplayer support out of the box
* Powered by **pymunk** physics
* Powered by **pyglet** for almost everything else
* Fun and simple

##Installation

There are a bunch of ways you can install **uberpong**:

### The *pip* way
```bash
pip3 install uberpong
uberpong # Create a session
uberpong -H 43.21.2.4 # Connect to someone else's session
```

###The *git* way
First of all, you must clone the repo ...
```bash
git clone https://github.com/axltxl/uberpong.git
cd uberpong
```

From this point you can run it standalone ...
```bash
pip3 install -r requirements.txt
./uberpong.sh # Create a session
./uberpong.sh -H 43.21.2.4 # Connect to someone else's session
```

###BTW: you need an opponent to play
By default, *uberpong* runs in server mode, if your opponent wishes
to join an existing *uberpong* session, he/she must do in client mode, like so:


```bash
uberpong -H <server ip address>
```

##Usage
```bash
uberpong [-H <ip_address> | --host <ip_address>] [--port <port> | -p <port>] [--lz4 | -z]
uberpong -h | --help
uberpong --version

Options:
    -z --lz4                    Use LZ4 compression algorithm
    -H --host <ip_address>      Server to connect to
    -p --port <port>            Port to connect to [default: 54212]
    -h --help                   Show this screen.
    --version                   Show version.
```

###Examples
* Dead-simple execution of the game
```bash
uberpong
```

* Connect to an existing session
```bash
uberpong -H <host ip address>
```

* Create a session using a different port number for listening
```bash
uberpong -p 54201
```

* Connect to a session listening on an arbitrary port number
```bash
uberpong -H <host ip address> -p 54201
```

* Activate lz4 compression for network traffic on you *uberpong* session
```bash
uberpong --lz4
```

* Connect to a session using lz4 network traffic compression
```bash
uberpong -H <host ip address> --lz4
```

##How to play
* Press `F12` to exit the game at any point
* In-Game: Press `W` to move your paddle up
* In-Game: Press `S` to move your paddle down


##Contributing
There are many ways in which you can contribute to *uberpong*.
Code patches are just one thing amongst others that you can submit to help the project.
We also welcome feedback, bug reports, feature requests, documentation improvements,
advertisement and testing.

##Third party assets
* 8-bit Operator+ font family is made by [Grandoplex Productions](http://grandchaos9000.deviantart.com)
* Some sounds were made by [Morten Barfod Søegaard, Little Robot Sound Factory](http://grandchaos9000.deviantart.com)
![](http://www.littlerobotsoundfactory.com/img/LittleRobotSoundFactory_Logo_00.png)

##Licensing
Please read the [LICENSE](https://github.com/axltxl/uberpong/blob/readme/LICENSE)
file bundled with this distribution

