## SLAY

This is a recreation of the game Slay, originally created by Sean O'Connor in 1995, But with over the internet* multiplayer using a server and client architecture

There are some key differences:

- Maps are randomly generated instead of preset and can be as large as you like**
- Units have fixed travel distance (2 cells)
- Theoretically infinite max players, but only upto 7 right now because i cant decide on good colors
- New Graphics and Sounds
- Game Replays are available

## Installation

The Built executables can be downloaded from the releases tab
There is a installer available for windows systems.
I am not able to test the code on other platforms but you should theoretically be able to download the .zip file and run the game

The game should be fully functional now and ill update the readme if any bugs are found
I doubt ill be working on this project any further

## Build Instructions

If you wish to build the code locally, The included build scripts in both Client and Server directories use pyinstaller to generate the executables
Also included is the installer build script based on WinRAR's CLI mode That was used to generate the sfx installer executable
Code was built using python ver 3.10.6

\*Requires Port Forwarding to connect to servers outside your local network<br>
\*\*At a certain point youll run out of screen space but if you have a widescreen, go ham.