<h1>SERVER INFO:</h1>

There should be a `config.ini` in the same directory as `Slay_Server.py` when you run it.
If it does not exist, it will automatically generate this file and then exit, Run it again to then launch the server

Config options are explained in the config file itself via comments

If excess clients try to connect, server will not respond
server logs all connections made, packets(as in messages) recieved and errors 

The server only has a very primitive anti-cheat and only checks to make sure moves are only made by the player whose turn it is
anything caught by this will be logged