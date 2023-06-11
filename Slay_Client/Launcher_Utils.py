from tkinter import *
from tkinter import ttk
from time import sleep
import os
import Slay
import Replayer
import webbrowser
import pathlib
import configparser
import importlib
import integratedServer.Constants
import integratedServer.Slay_Server
import integratedServer.Net_Utils
import integratedServer.Hex_Utils
import integratedServer.AI_Player
import integratedServer.AI_Utils
from Replay_Utils import getReplays
from Networking import connect, disconnect, closeDiscovery, getServers
from Net_Utils import status,type,address,players
from socket import gethostbyname

pathtopdf = r'file://' + str(pathlib.Path().resolve()/ 'Slay_Assets' / 'Help.pdf')

class MainWindow:

    def __init__(self,executor) -> None:
        
        self.executor = executor

        self.gameslist = []
        self.custom_server = []
        self.disabled = False
        self.selected_server = None
        self.scandata = []
        self.scanips = []
        self.scancall = 0
        self.settings = {}

        self.window = Tk()
        self.window.title('Slay Launcher')
        self.window.iconbitmap('icon.ico')
        self.window.resizable(False,False)
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)
        self.window.bind('<<StartGame>>',self.StartGame)
        self.window.bind('<<EnableUI>>',self.EnableUI)
        self.window.bind('<<DisableUI>>',self.DisableUI)
        self.window.protocol("WM_DELETE_WINDOW", self.windowClosed)

        self.mainframe = ttk.Frame(self.window,padding="3 3 12 24")
        self.mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        
        self.creditLabel = ttk.Label(self.window,text='Made by Shiven Bajpai',font=('Helvetica',8),padding='0 0 8 8')
        self.creditLabel.grid(column=0, row=1, sticky=(E,S))

        self.header = ttk.Label(self.mainframe,text='Slay!',font=('Helvetica',36),padding='0 10 0 20')
        self.header.grid(column=2,row=1,sticky=(N))

        self.buttonframe = ttk.Frame(self.mainframe,padding="0 0 15 24")
        self.buttonframe.grid(column=1, row=3,columnspan=3, sticky=(N))

        '''self.connect_button = ttk.Button(self.buttonframe, text='Connect', command=self.ConnectButtonPress, padding='0 2 0 2',width=30)
        self.connect_button.grid(column=1,row=1,columnspan=2,sticky=(E))
        self.connect_button.configure(state='disabled')

        self.direct_connect_button = ttk.Button(self.buttonframe, text='Direct Connect', command=self.DirectConnectButtonPress, padding='0 2 0 2',width=30)
        self.direct_connect_button.grid(column=3,row=1,columnspan=2,sticky=(N),padx=(8,8))

        self.server_button = ttk.Button(self.buttonframe, text='Start Game On Lan', command=self.ServerButtonPress, padding='0 2 0 2',width=30)
        self.server_button.grid(column=5,row=1,columnspan=2,sticky=(W))

        self.settings_button = ttk.Button(self.buttonframe, text='Settings', command=self.SettingsButtonPress, padding='0 2 0 2',width=45)
        self.settings_button.grid(column=1,row=2,columnspan=3,sticky=(E),pady=(8,8),padx=(4,4))
        
        self.replays_button = ttk.Button(self.buttonframe, text='Replays', command=self.ReplayButtonPress, padding='0 2 0 2',width=45)
        self.replays_button.grid(column=4,row=2,columnspan=3,sticky=(W),pady=(8,8),padx=(4,4))

        self.help_button = ttk.Button(self.buttonframe, text='Help↗', command=self.HelpButtonPress, padding='0 2 0 2',width=45)
        self.help_button.grid(column=1,row=3,columnspan=3,sticky=(E),padx=(4,4))

        self.credits_button = ttk.Button(self.buttonframe, text='Credits', command=self.CreditsButtonPress, padding='0 2 0 2',width=45)
        self.credits_button.grid(column=4,row=3,sticky=(W),columnspan=3,padx=(4,4))'''

        #MARKER

        self.connect_button = ttk.Button(self.buttonframe, text='Connect', command=self.ConnectButtonPress, padding='0 2 0 2',width=90)
        self.connect_button.grid(column=1,row=1,columnspan=6,sticky=(N),padx=(8,8))
        self.connect_button.configure(state='disabled')

        self.direct_connect_button = ttk.Button(self.buttonframe, text='Direct Connect', command=self.DirectConnectButtonPress, padding='0 2 0 2',width=90)
        self.direct_connect_button.grid(column=1,row=2,columnspan=6,sticky=(N),padx=(8,8),pady=(8,8))

        self.server_button = ttk.Button(self.buttonframe, text='Start Game On LAN', command=self.ServerButtonPress, padding='0 2 0 2',width=90)
        self.server_button.grid(column=1,row=3,columnspan=6,sticky=(N),padx=(8,8))

        self.settings_button = ttk.Button(self.buttonframe, text='Settings', command=self.SettingsButtonPress, padding='0 2 0 2',width=44)
        self.settings_button.grid(column=1,row=4,columnspan=3,sticky=(E),pady=(8,8),padx=(3,3))
        
        self.replays_button = ttk.Button(self.buttonframe, text='Replays', command=self.ReplayButtonPress, padding='0 2 0 2',width=44)
        self.replays_button.grid(column=4,row=4,columnspan=3,sticky=(W),pady=(8,8),padx=(3,3))

        self.help_button = ttk.Button(self.buttonframe, text='Help↗', command=self.HelpButtonPress, padding='0 2 0 2',width=44)
        self.help_button.grid(column=1,row=5,columnspan=3,sticky=(E),padx=(3,3))

        self.credits_button = ttk.Button(self.buttonframe, text='Credits', command=self.CreditsButtonPress, padding='0 2 0 2',width=44)
        self.credits_button.grid(column=4,row=5,sticky=(W),columnspan=3,padx=(3,3))

        self.status = StringVar()
        self.status_label = ttk.Label(self.mainframe,textvariable=self.status,padding='0 8 0 0')
        self.status_label.grid(column=2, row=4, sticky=(N))

        self.initServerlist()
        self.Loadsettings()
        self.window.after(500,self.ScanforGames)
        self.window.mainloop()

    def ScanforGames(self) -> None:
        
        if self.scancall == 5:
            pre_select = None if self.selected_server is None else self.selected_server[2][1]
            #if self.selected_server is not None: pre_select = self.selected_server[2][1]

            self.window.after(2000,self.ScanforGames)
            if len(self.scandata) == 0:
                for item in self.tree.get_children(): self.tree.delete(item)
                self.gameslist = []
                self.tree.insert('', 'end', text="1")
                self.tree.insert('', 'end', text="2")
                self.tree.insert('', 'end', text="3", values=('\t\t\t         Any', 'Servers on Your local network Show', 'Up Here', ''))
                self.tree.configure(selectmode='none')
            else:
                for item in self.tree.get_children(): self.tree.delete(item)
                self.gameslist = []
                for idx, item in enumerate(self.scandata):
                    self.tree.insert('','end',text=str(idx),values=(item.Name,address(item.Address),players(item.Players),status(item.Status),type(item.Type),500),iid=idx)
                    self.gameslist.append((item.Address,item.Type))
                    if pre_select == address(item.Address): 
                        self.tree.focus(idx)
                        self.tree.selection_set(idx)
                if not self.disabled: self.tree.configure(selectmode='browse')
                    

            self.scandata = []
            self.scanips = []
            self.scancall = 0
        else:
            getServers(self.scandata,self.scanips)
            self.scancall += 1
            self.window.after(50,self.ScanforGames)

    def initServerlist(self) -> None:
        self.treeFrame = ttk.Frame(self.mainframe,padding="0 25 0 15")
        self.treeFrame.grid(column=1,row=2,columnspan=3,sticky=(N),padx=(50,50))
        tree = ttk.Treeview(self.treeFrame, column=("c1", "c2", "c3","c4","c5"), show='headings', height=5)
        tree.pack(side='left')
        vsb = ttk.Scrollbar(self.treeFrame, orient="vertical", command=tree.yview)
        vsb.pack(side='right', fill='y')
        tree.configure(yscrollcommand = vsb.set)

        tree.column("# 1", anchor=W, width=200)
        tree.heading("# 1", text="Name", anchor=W)
        tree.column("# 2", anchor=W, width=200)
        tree.heading("# 2", text="Address", anchor=W)
        tree.column("# 3", anchor=W, width=55)
        tree.heading("# 3", text="Players", anchor=W)
        tree.column("# 4", anchor=W, width=100)
        tree.heading("# 4", text="Status", anchor=W)
        tree.column("# 5", anchor=W, width=50)
        tree.heading("# 5", text="Type", anchor=W)

        tree.insert('', 'end', text="1")
        tree.insert('', 'end', text="2")
        tree.insert('', 'end', text="3", values=('\t\t\t         Any', 'Servers on Your local network Show', 'Up Here', ''))

        tree.bind('<<TreeviewSelect>>',self.handleServerlistSelection)
        tree.configure(selectmode='none')

        self.tree = tree

    def handleServerlistSelection(self,event) -> None:
        if self.disabled: return
        if self.tree.focus() == '': 
            self.selected_server = None
            self.connect_button.configure(state='disabled')
        else: 
            if self.connect_button.config()['state'][-1] != 'enabled': self.connect_button.configure(state='enabled')
            self.selected_server = list(self.tree.item(self.tree.focus()).values())
    
    def Loadsettings(self) -> None:
        DEFAULTCONFIG = '''[SETTINGS]
        volume = 65
        debug = False
        freeze = False'''

        if os.path.exists('./config.ini'):
            config = configparser.ConfigParser()
            config.read('config.ini')
            self.settings['volume'] = int(config['SETTINGS']['volume'])
            self.settings['debug'] = config['SETTINGS']['debug'] == 'True'
            self.settings['freeze'] = config['SETTINGS']['freeze'] == 'True'
        else:
            self.settings['volume'] = 65
            self.settings['debug'] = False
            self.settings['freeze'] = False
            with open('./config.ini','x') as f: f.write(DEFAULTCONFIG) 

    def ConnectButtonPress(self) -> None:
        self.StartGame(custom=False)

    def DirectConnectButtonPress(self) -> None:
        self.window.event_generate('<<DisableUI>>')
        self.connection_window = ConnectionPopUp(self.window,self.custom_server)

    def SettingsButtonPress(self) -> None:
        self.window.event_generate('<<DisableUI>>')
        SettingsWindow(self.window,self.UpdateSettings,self.settings)

    def UpdateSettings(self,settings) -> None:
        for key in settings.keys():
            self.settings[key] = settings[key].get()

        newconfig = configparser.ConfigParser()
        newconfig['SETTINGS'] = {}
        for key,value in self.settings.items(): newconfig['SETTINGS'][key] = str(value)

        with open('./config.ini','w') as f: newconfig.write(f)

    def HelpButtonPress(self) -> None:
        webbrowser.open_new(pathtopdf)

    def CreditsButtonPress(self) -> None:
        self.window.event_generate('<<DisableUI>>')
        CreditsWindow(self.window)
        
    def ServerButtonPress(self) -> None:
        self.window.event_generate('<<DisableUI>>')
        integratedServerWindow(self.window,self.executor,self.run,(self.status,self.status_label))

    def ReplayButtonPress(self) -> None:
        self.window.event_generate('<<DisableUI>>')
        ReplayWindow(self.window,self.StartReplay)

    def StartReplay(self,selection) -> None:
        self.window.event_generate('<<DisableUI>>')
        self.status.set('Playing Replay')
        self.status_label.configure(foreground='green')
        self.executor.submit(Replayer.main,selection,self.settings).add_done_callback(self.handleGameReturn)

    def StartGame(self,x=None,custom=True) -> None:
        self.window.event_generate('<<DisableUI>>')
        try: del self.connection_window
        except (Exception) as err: pass

        if custom:
            try:
                ip = gethostbyname(self.custom_server[0])
                print(ip)
            except (Exception):
                print('gaierror')
                self.status.set('Error resolving address,\ntry again if the issue \npersists,you have the wrong \naddress')
                self.status_label.configure(foreground='red')
                self.window.event_generate('<<EnableUI>>')
                return

            info = connect(ip,self.custom_server[1],info_req=True)
            if info.__class__ == tuple:
                self.status.set(info[0])
                self.status_label.configure(foreground='red')
                self.window.event_generate('<<EnableUI>>')
                return
            if not info['public']: PasswordPopUp(self.window,(self.run,self.custom_server))
            else: self.run(self.custom_server)
        else:
            if not self.gameslist[int(self.selected_server[0])][1]:
                PasswordPopUp(self.window,(self.run,self.gameslist[int(self.selected_server[0])][0]))
            self.run(self.gameslist[int(self.selected_server[0])][0])

    def handleGameReturn(self,future) -> None:
        result, success = future.result()

        disconnect()
        self.raise_above_all()

        self.status.set(result)
        if success: self.status_label.configure(foreground='green')
        else: self.status_label.configure(foreground='red')
        self.window.event_generate('<<EnableUI>>')

    def run(self,server,password=None) -> None:
        self.window.event_generate('<<DisableUI>>')
        ip,port = server
        
        if port<1 or port>65535:
            self.status.set('Invalid port')
            self.status_label.configure(foreground='red')
            return

        try:
            ip = gethostbyname(ip)
        except (Exception):
            print('gaierror')
            self.status.set('Error resolving address,\ntry again if the issue \npersists,you have the wrong \naddress')
            self.status_label.configure(foreground='red')
            return

        self.status.set('Connecting...')
        self.status_label.configure(foreground='red')
        self.window.update_idletasks()
        self.window.update()

        result, color, config = connect(ip,port,password=password)

        if color == None:
            self.status.set(result)
            self.window.event_generate('<<EnableUI>>')
            return

        self.status.set('Running')
        self.status_label.configure(foreground='green')
        self.window.update_idletasks()
        self.window.update()

        config.update(self.settings)
        config['volume'] = config['volume'] / 100
        self.executor.submit(Slay.main,color,config).add_done_callback(self.handleGameReturn)

    def EnableUI(self,x=None):
        self.disabled = False
        self.direct_connect_button.configure(state='enabled')
        if self.selected_server != None: self.connect_button.configure(state='enabled')
        self.settings_button.configure(state='enabled')
        self.help_button.configure(state='enabled')
        self.credits_button.configure(state='enabled')
        self.replays_button.configure(state='enabled')
        self.server_button.configure(state='enabled')
        self.tree.configure(selectmode='browse')

    def DisableUI(self,x=None):
        self.disabled = True
        self.direct_connect_button.configure(state='disabled')
        self.connect_button.configure(state='disabled')
        self.settings_button.configure(state='disabled')
        self.help_button.configure(state='disabled')
        self.credits_button.configure(state='disabled')
        self.replays_button.configure(state='disabled')
        self.server_button.configure(state='disabled')
        self.tree.configure(selectmode='none')
        self.window.update_idletasks()

    def windowClosed(self) -> None:
        disconnect()
        closeDiscovery()
        self.window.destroy()

    def raise_above_all(self) -> None:
        self.window.attributes('-topmost', 1)
        self.window.attributes('-topmost', 0)

class ConnectionPopUp:
    def __init__(self,mainWindow: Toplevel,returnObject: list) -> None:
        
        self.mainWindow = mainWindow
        self.returnObject = returnObject
        self.window = Toplevel(mainWindow)
        self.window.title('Slay - Direct Connect')
        self.window.iconbitmap('icon.ico')
        self.window.resizable(False,False)
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)
        self.window.protocol("WM_DELETE_WINDOW", self.windowClosed)

        self.mainframe = ttk.Frame(self.window,padding="3 3 12 12")
        self.mainframe.grid(column=0, row=0, sticky=(N, W, E, S))

        self.header = ttk.Label(self.mainframe,text='Direct Connection',font=('Helvetica',18),padding='0 15 0 15')
        self.header.grid(column=3,row=1,columnspan=2,sticky=(N))

        self.ip_field = StringVar()
        self.port_field = IntVar()
        self.status = StringVar()

        ttk.Label(self.mainframe,text='Hostname: ',padding='45 0 0 0').grid(column=1,row=2,columnspan=2,sticky=(E))
        host_entry = ttk.Entry(self.mainframe,textvariable=self.ip_field,width=30)
        host_entry.grid(column=3,row=2,columnspan=2,sticky=(W))
        self.ip_field.set('127.0.0.1')
        ttk.Label(self.mainframe,text='Port: ',padding='0 0 0 0').grid(column=5,row=2,sticky=(W))
        port_entry = ttk.Entry(self.mainframe,textvariable=self.port_field,width=7)
        port_entry.grid(column=6,row=2,sticky=(E))
        self.port_field.set(4444)
        ttk.Label(self.mainframe,text='',padding='0 0 15 15').grid(column=7,row=2)

        connectButton = ttk.Button(self.mainframe, text="Connect", command=self.ConnectButtonPress, padding='0 2 0 2',width=30)
        connectButton.grid(column=3, row=3, columnspan=2,sticky=(N))

        self.window.mainloop()

    def ConnectButtonPress(self) -> None:
        self.returnObject.clear()
        self.returnObject.extend([self.ip_field.get(),self.port_field.get()])
        self.mainWindow.event_generate('<<EnableUI>>')
        self.window.destroy()
        self.mainWindow.event_generate('<<StartGame>>')

    def windowClosed(self) -> None:
        self.mainWindow.event_generate('<<EnableUI>>')
        self.window.destroy()

class PasswordPopUp:

    def __init__(self,mainWindow: Toplevel,runFunction: list) -> None:
        
        self.mainWindow = mainWindow
        self.runFunction = runFunction
        self.window = Toplevel(mainWindow)
        self.window.title('Slay - Enter Password')
        self.window.iconbitmap('icon.ico')
        self.window.resizable(False,False)
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)
        self.window.protocol("WM_DELETE_WINDOW", self.windowClosed)

        self.mainframe = ttk.Frame(self.window,padding="3 3 12 12")
        self.mainframe.grid(column=0, row=0, sticky=(N, W, E, S))

        self.header = ttk.Label(self.mainframe,text='Enter Password to join game',font=('Helvetica',18),padding='0 15 0 15')
        self.header.grid(column=1,row=1,columnspan=3,sticky=(N))

        self.pass_field = StringVar()

        ttk.Label(self.mainframe,text='Password: ').grid(column=1,row=2,sticky=(E),padx=(45,0))
        host_entry = ttk.Entry(self.mainframe,textvariable=self.pass_field,width=30)
        host_entry.grid(column=2,row=2,sticky=(W),padx=(0,45))

        ConnectButton = ttk.Button(self.mainframe, text="Connect", command=self.ConnectButtonPressed, padding='0 2 0 2',width=30)
        ConnectButton.grid(column=2, row=3,sticky=(N,W),pady=(8,20),padx=(0,0))

        self.window.mainloop()


    def windowClosed(self) -> None:
        self.mainWindow.event_generate('<<EnableUI>>')
        self.window.destroy()

    def ConnectButtonPressed(self) -> None:
        self.window.destroy()
        self.mainWindow.after(100,self.runFunction[0],self.runFunction[1],self.pass_field.get())

class SettingsWindow: 
    def __init__(self,mainWindow: Toplevel,setting_setter,current_settings) -> None:
        
        self.setter = setting_setter
        self.settings = {'volume': IntVar(value=current_settings['volume']),
                         'debug': BooleanVar(value=current_settings['debug']),
                         'freeze': BooleanVar(value=current_settings['freeze'])}

        self.mainWindow = mainWindow
        self.window = Toplevel(mainWindow)
        self.window.title('Slay - Settings')
        self.window.iconbitmap('icon.ico')
        self.window.resizable(False,False)
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)
        self.window.protocol("WM_DELETE_WINDOW", self.windowClosed)

        self.mainframe = ttk.Frame(self.window,padding="3 3 12 12")
        self.mainframe.grid(column=0, row=0, sticky=(N, W, E, S))

        self.header = ttk.Label(self.mainframe,text='Settings',font=('Helvetica',22),padding='50 25 50 15')
        self.header.grid(column=1,row=1,columnspan=3,sticky=(N))

        self.soundFrame = ttk.Frame(self.mainframe,padding="12 12 12 12",borderwidth=1, relief="solid")
        self.soundFrame.grid(column=1,row=2,columnspan=2,padx=(10,10))
        ttk.Label(self.soundFrame,text='Sound Settings:',font=('default',12),padding='0 0 0 12').grid(column=1,row=1,sticky=(S,E))
        ttk.Label(self.soundFrame,text='Master Volume:',padding='0 0 0 4').grid(column=1,row=2,sticky=(S,E))
        self.soundScale = Scale(self.soundFrame, from_=0, to=100, orient=HORIZONTAL,variable=self.settings['volume'])
        self.soundScale.grid(column=2,row=2,sticky=(S,W))

        self.devFrame = ttk.Frame(self.mainframe,padding="12 12 12 12",borderwidth=1, relief="solid")
        self.devFrame.grid(column=1,row=3,columnspan=2,padx=(10,10),pady=(10,10),sticky=(N,W,E))
        ttk.Label(self.devFrame,text='Developer Settings:',font=('default',12),padding='0 0 0 12').grid(column=1,row=1,sticky=(S,E))
        self.debugCheckbox = ttk.Checkbutton(self.devFrame, text='Enable Debugger' ,variable=self.settings['debug'],onvalue=True,offvalue=False)
        self.debugCheckbox.grid(column=1,row=2,sticky=(S,W))
        self.freezeCheckbox = ttk.Checkbutton(self.devFrame, text='Freeze game on crash' ,variable=self.settings['freeze'],onvalue=True,offvalue=False)
        self.freezeCheckbox.grid(column=1,row=3,sticky=(S,W))

        self.window.mainloop()

    def windowClosed(self) -> None:
        self.mainWindow.event_generate('<<EnableUI>>')
        self.mainWindow.after_idle(self.setter,self.settings)
        self.window.destroy()

class ReplayWindow:
    def __init__(self,mainWindow,playFunction) -> None:
        self.mainWindow = mainWindow
        self.playFunction = playFunction
        self.selection = None

        self.window = Toplevel(mainWindow)
        self.window.title('Slay - Replays')
        self.window.iconbitmap('icon.ico')
        self.window.resizable(False,False)
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)
        self.window.protocol("WM_DELETE_WINDOW", self.windowClosed)

        self.mainframe = ttk.Frame(self.window,padding="3 3 12 12")
        self.mainframe.grid(column=0, row=0, sticky=(N, W, E, S))

        self.header = ttk.Label(self.mainframe,text='Replays',font=('Helvetica',22),padding='50 25 50 15')
        self.header.grid(column=1,row=1,columnspan=3,sticky=(N))

        self.infotext = ttk.Label(self.mainframe,text='Select a replay by date:',font=('Helvetica',8))
        self.infotext.grid(column=1,row=2,columnspan=1,sticky=(W),padx=(15,0),pady=(5,5))

        self.replayList = getReplays()
        self.listbox = Listbox(self.mainframe,height=8,width=40)
        self.listbox.grid(column=1,row=3,sticky=(N),pady=(5,5),padx=(5,5))
        self.listbox.configure(selectmode='browse')
        self.listbox.bind('<<ListboxSelect>>',self.selectionHandler)
        for item in self.replayList: self.listbox.insert('end',item)

        self.confirmBox = ttk.Button(self.mainframe,command=self.confirmPress,text='Play')
        self.confirmBox.grid(column=1,row=4,sticky=(N),pady=(5,5))

        self.window.mainloop()
    
    def confirmPress(self) -> None:
        self.windowClosed()
        if self.selection is not None: self.playFunction(self.selection)

    def selectionHandler(self,_) -> None:
        if len(self.listbox.curselection()) == 0: 
            self.selection = None
            self.confirmBox.configure(state='disabled')
        else:
            self.selection = self.replayList[self.listbox.curselection()[0]]
            self.confirmBox.configure(state='enabled')

    def windowClosed(self) -> None:
        self.mainWindow.event_generate('<<EnableUI>>')
        self.window.destroy()

class CreditsWindow:
    def __init__(self,mainWindow: Toplevel) -> None:
        
        self.mainWindow = mainWindow
        self.window = Toplevel(mainWindow)
        self.window.title('Slay - Credits')
        self.window.iconbitmap('icon.ico')
        self.window.resizable(False,False)
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)
        self.window.protocol("WM_DELETE_WINDOW", self.windowClosed)

        self.mainframe = ttk.Frame(self.window,padding="3 3 12 12")
        self.mainframe.grid(column=0, row=0, sticky=(N, W, E, S))

        self.header = ttk.Label(self.mainframe,text='Credits',font=('Helvetica',22),padding='0 15 0 15')
        self.header.grid(column=1,row=1,columnspan=3,sticky=(N))

        self.text = ttk.Label(self.mainframe,text='This was created by me Shiven Bajpai for\n a computer science project\n\nOriginal Game made by Sean\'O Connor and a official remake is available\n for purchase on steam today\n\nAll graphics are my own\nSounds from freesound.org and mixit.co'.center(72))
        self.text.grid(column=2,row=2,sticky=(N),pady=(35,25))
        self.window.mainloop()


    def windowClosed(self) -> None:
        self.mainWindow.event_generate('<<EnableUI>>')
        self.window.destroy()

class integratedServerWindow:

    MINIMUM_SIZES = [None,None,9,9,24,49,90,144,256,361,484]
    MIN_SIZE = 4

    def __init__(self,mainWindow: Toplevel,executor,runCallback,status_label) -> None:
        
        self.mainWindow = mainWindow
        self.executor = executor
        self.runCallback = runCallback
        self.mainWindowStatusLabel = status_label
        self.window = Toplevel(mainWindow)
        self.window.title('Slay - Start Local Game')
        self.window.iconbitmap('icon.ico')
        self.window.resizable(False,False)
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)
        self.window.protocol("WM_DELETE_WINDOW", self.windowClosed)

        self.loadSettings()

        self.mainframe = ttk.Frame(self.window,padding="3 3 12 12")
        self.mainframe.grid(column=0, row=0, sticky=(N, W, E, S))

        self.header = ttk.Label(self.mainframe,text='Pick settings to start game on LAN',font=('Helvetica',22),padding='50 25 50 15')
        self.header.grid(column=1,row=1,columnspan=2,sticky=(N,W))

        self.serverFrame = ttk.Frame(self.mainframe,padding="12 12 12 12",borderwidth=1, relief="solid")
        self.serverFrame.grid(column=1,row=2,columnspan=2,padx=(10,10),sticky=(W,E))
        ttk.Label(self.serverFrame,text='Server Settings:',font=('default',12),padding='0 0 0 12').grid(column=1,row=1,sticky=(S,W))

        ttk.Label(self.serverFrame,text='Port:',padding='0 0 0 4').grid(column=1,row=2,sticky=(S,E))
        self.portField = ttk.Entry(self.serverFrame,textvariable=self.settings['PORT'],width=7)
        self.portField.grid(column=2,row=2,sticky=(S,W))

        ttk.Label(self.serverFrame,text='Password (Leave empty for none):',padding='0 0 0 4').grid(column=1,row=3,sticky=(S,E))
        self.passField = ttk.Entry(self.serverFrame,textvariable=self.settings['PASSWORD'],width=30)
        self.passField.grid(column=2,row=3,sticky=(S,W))

        self.discoveryCheckbox = ttk.Checkbutton(self.serverFrame, text='Enable Discovery over LAN' ,variable=self.settings['DISCOVERABLE'],onvalue=True,offvalue=False,command=self.discoveryToggle)
        self.discoveryCheckbox.grid(column=1,row=4,sticky=(S,E))

        ttk.Label(self.serverFrame,text='Server Name:',padding='0 0 0 4').grid(column=1,row=5,sticky=(S,E))
        self.nameField = ttk.Entry(self.serverFrame,textvariable=self.settings['NAME'],width=30)
        self.nameField.grid(column=2,row=5,sticky=(S,W))


        self.gameFrame = ttk.Frame(self.mainframe,padding="12 12 12 12",borderwidth=1, relief="solid")
        self.gameFrame.grid(column=1,row=3,columnspan=2,padx=(10,10),pady=(10,10),sticky=(N,W,E))
        ttk.Label(self.gameFrame,text='Game Settings:',font=('default',12),padding='0 0 0 12').grid(column=1,row=1,sticky=(S,W))

        ttk.Label(self.gameFrame,text='Map Size (X):',padding='0 0 0 4').grid(column=1,row=2,sticky=(S,E))
        self.XSlider = Scale(self.gameFrame, from_=5, to=25, orient=HORIZONTAL,variable=self.settings['XSIZE'],command=self.SizeUpdate)
        self.XSlider.grid(column=2,row=2,sticky=(S,W))

        ttk.Label(self.gameFrame,text='Map Size (Y):',padding='0 0 0 4').grid(column=1,row=3,sticky=(S,E))
        self.YSlider = Scale(self.gameFrame, from_=5, to=25, orient=HORIZONTAL,variable=self.settings['YSIZE'],command=self.SizeUpdate)
        self.YSlider.grid(column=2,row=3,sticky=(S,W))

        ttk.Label(self.gameFrame,text='No. Of Players:',padding='0 0 0 4').grid(column=1,row=4,sticky=(S,E))
        self.PlayerSlider = Scale(self.gameFrame, from_=2, to=10, orient=HORIZONTAL,variable=self.settings['MAX_COLOR'],command=self.playersSliderUpdate)
        self.PlayerSlider.grid(column=2,row=4,sticky=(S,W))

        ttk.Label(self.gameFrame,text='No. Of Bots:',padding='0 0 0 4').grid(column=1,row=5,sticky=(S,E))
        self.BotSlider = Scale(self.gameFrame, from_=0, to=10, orient=HORIZONTAL,variable=self.settings['BOTS'])
        self.BotSlider.grid(column=2,row=5,sticky=(S,W))

        self.buttonFrame = ttk.Frame(self.mainframe,padding="12 12 12 12",borderwidth=1)
        self.buttonFrame.grid(column=1,row=4,columnspan=2,padx=(10,10),pady=(10,10),sticky=(N))
        
        self.statusTextVar = StringVar(self.buttonFrame,value='')
        self.statusText = ttk.Label(self.buttonFrame,textvariable=self.statusTextVar,padding='0 0 0 4',foreground='red')
        self.statusText.grid(column=1,row=1,columnspan=2,sticky=(N))

        self.connectButton = ttk.Button(self.buttonFrame, text="Start & Join", command=self.confirmPress, padding='0 2 0 2',width=30)
        self.connectButton.grid(column=1, row=2,sticky=(N,E))
        self.cancelButton = ttk.Button(self.buttonFrame, text="Cancel", command=self.windowClosed, padding='0 2 0 2',width=30)
        self.cancelButton.grid(column=2, row=2,sticky=(N,W))

        self.playersSliderUpdate()
        self.window.mainloop()

    def discoveryToggle(self) -> None:
        self.nameField.configure(state=('enabled' if self.settings['DISCOVERABLE'].get() else 'disabled'))

    def playersSliderUpdate(self,_=None) -> None:
        if self.settings['BOTS'].get() >= self.settings['MAX_COLOR'].get():
            self.settings['BOTS'].set(self.settings['MAX_COLOR'].get() - 1)
        
        self.BotSlider.configure(to=self.settings['MAX_COLOR'].get()-1)

        self.SizeUpdate()

    def SizeUpdate(self,e=None) -> None:
        if self.settings['XSIZE'].get() * self.settings['YSIZE'].get() < self.MINIMUM_SIZES[self.settings['MAX_COLOR'].get()]:
            self.statusTextVar.set(f'Map Size too small(<{self.MINIMUM_SIZES[self.settings["MAX_COLOR"].get()]}), increase to start')
            self.connectButton.configure(state='disabled')
        else:
            self.statusTextVar.set(f'')
            self.connectButton.configure(state='enabled')

    def windowClosed(self) -> None:
        self.saveSettings()
        self.mainWindow.event_generate('<<EnableUI>>')
        self.window.destroy()

    def confirmPress(self) -> None:
        self.windowClosed()
        importlib.reload(integratedServer.Constants)
        importlib.reload(integratedServer.Net_Utils)
        importlib.reload(integratedServer.AI_Utils)
        importlib.reload(integratedServer.AI_Player)
        importlib.reload(integratedServer.Hex_Utils)
        importlib.reload(integratedServer.Slay_Server)
        self.executor.submit(integratedServer.Slay_Server.main)
        self.mainWindowStatusLabel[0].set('Waiting for server to start...')
        self.mainWindowStatusLabel[1].configure(foreground='red')
        self.mainWindow.event_generate('<<DisableUI>>')
        sleep(0.5*self.settings["MAX_COLOR"].get())
        self.runCallback(('localhost',int(self.settings['PORT'].get())),self.settings['PASSWORD'].get())

    def loadSettings(self) -> None:

        DEFAULTCONFIG = '''[BASIC]
# Port on which server listens, ports 0-1023 are privileged and may require elevated access
Port = 4444

# Map size in number of cells, too many the window might be too big
# Also larger maps take much longer to generate
MapXSize = 15
MapYSize = 15

# Number of players needed for the game and the number of bots in the game (there must be atleast one human player)
NumberOfPlayers = 2
NumberofBots = 0

# Automatically-Relaunch server every time game ends/crashes
AutoReboot = False

[DISCOVERY]
# Allow other computers on the local network to find and connect to this server
# If set to False, all discovery related options are meaningless
EnableDiscovery = True

# Name of server in server list on client side
DiscoveryServerName = Slay Server

# Password required to join
# If empty, password will not be required
Password = 

[ADVANCED]
# Dont touch unless you know what you're doing
# IP on which server socket requests to listen
IP = 0.0.0.0'''

        self.settings = {}
        self.settings['PORT'] = StringVar(value='4444')
        self.settings['XSIZE'] = IntVar(value=15)
        self.settings['YSIZE'] = IntVar(value=15)
        self.settings['MAX_COLOR'] = IntVar(value=2)
        self.settings['BOTS'] = IntVar(value=0)
        self.settings['DISCOVERABLE'] = BooleanVar(value=True)
        self.settings['NAME'] = StringVar(value='Local Slay Server')
        self.settings['PASSWORD'] = StringVar(value='')

        if os.path.exists('./integratedServer/config.ini'):
            config = configparser.ConfigParser()
            config.read('./integratedServer/config.ini')
            self.settings['PORT'].set(str(config['BASIC']['Port']))
            self.settings['XSIZE'].set(int(config['BASIC']['MapXSize']))
            self.settings['YSIZE'].set(int(config['BASIC']['MapYSize']))
            self.settings['MAX_COLOR'].set(int(config['BASIC']['NumberOfPlayers']))
            self.settings['BOTS'].set(int(config['BASIC']['NumberOfBots']))
            self.settings['DISCOVERABLE'].set(config['DISCOVERY']['EnableDiscovery'] == 'True')
            self.settings['NAME'].set(config['DISCOVERY']['DiscoveryServerName'])
            self.settings['PASSWORD'].set(config['DISCOVERY']['Password'])
        else:
            with open('./config.ini','x') as f: f.write(DEFAULTCONFIG)
            self.windowClosed()

    def saveSettings(self) -> None:

        config = configparser.ConfigParser()
        config.read('./integratedServer/config.ini')

        config['BASIC']['Port'] = str(self.settings['PORT'].get())
        config['BASIC']['MapXSize'] = str(self.settings['XSIZE'].get())
        config['BASIC']['MapYSize'] = str(self.settings['YSIZE'].get())
        config['BASIC']['NumberOfPlayers'] = str(self.settings['MAX_COLOR'].get())
        config['BASIC']['NumberOfBots'] = str(self.settings['BOTS'].get())
        config['DISCOVERY']['EnableDiscovery'] = str(self.settings['DISCOVERABLE'].get())
        config['DISCOVERY']['DiscoveryServerName'] = str(self.settings['NAME'].get())
        config['DISCOVERY']['Password'] = str(self.settings['PASSWORD'].get())

        with open('./integratedServer/config.ini','w') as f: config.write(f)