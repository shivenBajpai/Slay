import webbrowser
import pathlib


pathtopdf = str(pathlib.Path().resolve()/ 'Slay_Client' / 'Slay_Assets' / 'Help.pdf')
webbrowser.open_new(pathtopdf)