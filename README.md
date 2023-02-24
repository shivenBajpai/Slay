## SLAY (W.I.P)

This is a recreation of the game Slay, originally created by Sean O'Connor in 1995, But with over the internet* multiplayer using a server and client architecture

This game is fully functional, although there are a couple bugs to be squashed and the help tab is not yet implemented

There are some differences in gameplay:

- Maps are randomly generated instead of preset
- Units have fixed travel distance (2 cells)
- Theoretically infinite max players** (NOT IMPLEMENTED, CURRENT MAX 4)
- New Graphics

To run the game, run New_Launcher.py in the Slay_Client directory

To start server run Slay_Server.py in Slay_Server directory

\*Requires Port Forwarding to connect to servers outside your local network<br>
\*\*Due to map generation taking much longer for high player counts, and due to more players requiring a map size that might make the window too big\<testing pending on this\>. In practice this gets limited to moderate number of players.

Created using python ver 3.10.6, if you have weird issues maybe updating python will help