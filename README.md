Uber Pong!
==========

An Uber-engineered overthought multiplayer implementation of a classic game,
or *How I Stopped Worrying about and Learned Python The Right Way*.

the image goes here

##Requirements
* [pyglet](http://pyglet.org)
* [pymunk](http://pymunk.org)
* [docopt](http://docopt.org)
* [lz4](http://lz4.org)
* [simpleubjson](http://simpleubjson.org)
* [bson](http://bson.org)

## Features
* You already know how to play
* Multiplayer support out of the box
* Powered by pymunk physics and pyglet
* Painless installation

##Installation

There are a bunch of ways you can install **uberpong**:

### The pip way
```
pip3 install uberpong
uberpong
```

###The git way
First of all, you must clone the repo ...
```
git clone https://github.com/axltxl/uberpong.git
cd uberpong
```

From this point you could either, run it stand-alone
```
pip3 install -r requirements.txt
./uberpong.sh
```

or just install it
```
# you could at this point do the following inside a pyvenv
# pyvenv .pyvenv && .pyvenv/bin/activate
pip3 install .
uberpong
```

###BTW: you need a companion to play
By default, uberpong run as a server, if you or your partner wish
to join an existing uberpong session, you can do it like so:


```
uberpong -H <server ip address>

##Usage
```
uberpong [options]
--host ADDRESS, -H ADDRESS  Server address to join [default: localhost]
--port NUMBER, -p NUMBER Server port [default: 6000]
--lz4, -z Enforce LZ4 compression on network traffic (experimental)
```


##How to play
* Press `F12` to exit the game at any point
* In-Game: Press `W` to move your paddle up
* In-Game: Press `S` to move your paddle down


##Contributing
There are many ways in which you can contribute to uberpong.
Code patches are just one thing amongst others that you can submit to help the proje
We also welcome feedback, bug reports, feature requests, documentation improvements,
advertisement and testing.

##Third party assets
Some sounds were made by *Morten Barfod Søegaard, Little Robot Sound Factory*
![](http://www.littlerobotsoundfactory.com/img/LittleRobotSoundFactory_Logo_00.png)

##Licensing
Please read the LICENSE file bundled with this distribution

