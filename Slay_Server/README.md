<h1>SERVER INFO:</h1>

There should be a `config.ini` in this directory when you run it.
If it does not exist, it will automatically generate this file.
All server config is performed in that file

If youre running the python code directly
It is recommended to run the server via `Supervisor.py` rather than running `Slay_Server.py`
The built executable will always run via `Supervisor.py`

If excess clients try to connect, server will not respond
server logs all connections made, packets(as in messages) recieved and errors 

The server only has a very primitive anti-cheat and only checks to make sure moves are only made by the player whose turn it is
anything caught by this will be logged