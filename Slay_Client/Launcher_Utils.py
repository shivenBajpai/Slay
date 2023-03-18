from tkinter import *
from tkinter import ttk
from concurrent.futures import ThreadPoolExecutor
import Slay
import Replayer
from Replay_Utils import getReplays
from Networking import connect, disconnect, closeDiscovery, getServers
from Net_Utils import status,type,address,players
from socket import gethostbyname

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
        self.volume = 75

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

        self.connect_button = ttk.Button(self.buttonframe, text='Connect', command=self.ConnectButtonPress, padding='0 2 0 2',width=30)
        self.connect_button.grid(column=1,row=1,sticky=(E))
        self.connect_button.configure(state='disabled')

        self.direct_connect_button = ttk.Button(self.buttonframe, text='Direct Connect', command=self.DirectConnectButtonPress, padding='0 2 0 2',width=30)
        self.direct_connect_button.grid(column=2,row=1,sticky=(N),padx=(8,8))

        self.settings_button = ttk.Button(self.buttonframe, text='Settings', command=self.SettingsButtonPress, padding='0 2 0 2',width=30)
        self.settings_button.grid(column=3,row=1,sticky=(W))

        self.help_button = ttk.Button(self.buttonframe, text='Help', command=self.HelpButtonPress, padding='0 2 0 2',width=30)
        self.help_button.grid(column=1,row=2,sticky=(E),pady=(8,0))

        self.credits_button = ttk.Button(self.buttonframe, text='Credits', command=self.CreditsButtonPress, padding='0 2 0 2',width=30)
        self.credits_button.grid(column=2,row=2,sticky=(E),padx=(8,8),pady=(8,0))

        self.replays_button = ttk.Button(self.buttonframe, text='Replays', command=self.ReplayButtonPress, padding='0 2 0 2',width=30)
        self.replays_button.grid(column=3,row=2,sticky=(E),pady=(8,0))

        self.status = StringVar()
        self.status_label = ttk.Label(self.mainframe,textvariable=self.status,padding='0 8 0 0')
        self.status_label.grid(column=2, row=4, sticky=(N))

        self.initServerlist()
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
            self.selected_server = list(self.tree.item(self.tree.focus()).values())
            self.connect_button.configure(state='enabled')
    
    def ConnectButtonPress(self) -> None:
        self.StartGame(custom=False)

    def DirectConnectButtonPress(self) -> None:
        self.window.event_generate('<<DisableUI>>')
        self.connection_window = ConnectionPopUp(self.window,self.custom_server)

    def SettingsButtonPress(self) -> None:
        self.window.event_generate('<<DisableUI>>')
        SettingsWindow(self.window,self.UpdateSettings,self.volume)

    def UpdateSettings(self,settings) -> None:
        self.volume = settings['volume'].get()
        print('set volume to',settings['volume'].get())

    def HelpButtonPress(self) -> None:
        print('Help pressed')

    def CreditsButtonPress(self) -> None:
        self.window.event_generate('<<DisableUI>>')
        CreditsWindow(self.window)

    def ReplayButtonPress(self) -> None:
        self.window.event_generate('<<DisableUI>>')
        ReplayWindow(self.window,self.StartReplay)

    def StartReplay(self,selection) -> None:
        self.window.event_generate('<<DisableUI>>')
        self.status.set('Playing Replay')
        self.status_label.configure(foreground='green')
        self.executor.submit(Replayer.main,selection).add_done_callback(self.handleGameReturn)

    def StartGame(self,x=None,custom=True) -> None:
        self.window.event_generate('<<DisableUI>>')
        try: del self.connection_window
        except (Exception) as err: pass
        print('Game Start initiated')
        if custom:
            info = connect(self.custom_server[0],self.custom_server[1],info_req=True)
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

        config['VOL'] = self.volume/100
        self.executor.submit(Slay.main,color,config).add_done_callback(self.handleGameReturn)

    def EnableUI(self,x=None):
        self.disabled = False
        self.direct_connect_button.configure(state='enabled')
        if self.selected_server != None: self.connect_button.configure(state='enabled')
        self.settings_button.configure(state='enabled')
        self.help_button.configure(state='enabled')
        self.credits_button.configure(state='enabled')
        self.replays_button.configure(state='enabled')
        self.tree.configure(selectmode='browse')

    def DisableUI(self,x=None):
        self.disabled = True
        self.direct_connect_button.configure(state='disabled')
        self.connect_button.configure(state='disabled')
        self.settings_button.configure(state='disabled')
        self.help_button.configure(state='disabled')
        self.credits_button.configure(state='disabled')
        self.replays_button.configure(state='disabled')
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
    def __init__(self,mainWindow: Toplevel,setting_setter,*current_settings) -> None:
        
        self.setter = setting_setter
        self.settings = {'volume':IntVar(value=current_settings[0])}

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

        self.window.mainloop()

    def windowClosed(self) -> None:
        self.mainWindow.event_generate('<<EnableUI>>')
        self.mainWindow.after_idle(self.setter,self.settings)
        self.window.destroy()

class HelpWindow: ...

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
        self.playFunction(self.selection)

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

        self.text = ttk.Label(self.mainframe,text='This was created by me Shiven Bajpai for\n a computer science project\n\nOriginal Game made by Sean\'O Connor and a official remake is available\n for purchase on steam today\n\nAll graphics are my own'.center(72))
        self.text.grid(column=2,row=2,sticky=(N),pady=(35,25))
        self.window.mainloop()


    def windowClosed(self) -> None:
        self.mainWindow.event_generate('<<EnableUI>>')
        self.window.destroy()

#TODO: Decide if this stays here or in the other file
if __name__ == '__main__':
    with ThreadPoolExecutor(max_workers=1,thread_name_prefix='SLAY') as exec:
        MainWindow(exec)