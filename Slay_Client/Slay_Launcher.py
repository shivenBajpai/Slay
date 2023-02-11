from tkinter import *
from tkinter import ttk
from Slay import main
from Networking import connect, getGrid, disconnect

def raise_above_all(window):
    window.attributes('-topmost', 1)
    window.attributes('-topmost', 0)

def run():

    ip,port = ip_field.get(),port_field.get()

    if len(ip) < 7: 
        status.set('Invalid ip')
        statusLabel.configure(foreground='red')
        return
    if ip.count('.') != 3:
        status.set('Invalid ip')
        statusLabel.configure(foreground='red')
        return
    if port<1 or port>65535:
        status.set('Invalid port')
        statusLabel.configure(foreground='red')
        return

    status.set('Connecting...')
    statusLabel.configure(foreground='red')
    connectButton.configure(state='disabled')
    window.update_idletasks()
    window.update()

    result, color, config = connect(ip,port)

    status.set(result)
    if color == None:
        connectButton.configure(state='enabled')
        return
    window.update_idletasks()
    window.update()

    grid = getGrid()

    status.set('Running')
    statusLabel.configure(foreground='green')
    window.update_idletasks()
    window.update()

    result, success = main(grid,color,config)

    disconnect()
    raise_above_all(window)

    status.set(result)
    if success: statusLabel.configure(foreground='green')
    else: statusLabel.configure(foreground='red')
    connectButton.configure(state='enabled')

window = Tk()
window.title('Slay Launcher')
window.iconbitmap('icon.ico')
window.resizable(False,False)

mainframe = ttk.Frame(window,padding="3 3 12 24")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
window.columnconfigure(0, weight=1)
window.rowconfigure(0, weight=1)

ttk.Label(mainframe,text='Slay!',font=('Helvetica',36),padding='0 10 0 20').grid(column=3,row=1,columnspan=2,sticky=(N))

ip_field = StringVar()
port_field = IntVar()
status = StringVar()

ttk.Label(mainframe,text='Enter IP: ',padding='45 0 0 0').grid(column=1,row=2,columnspan=2,sticky=(E))
ttk.Entry(mainframe,textvariable=ip_field,width=30).grid(column=3,row=2,columnspan=2,sticky=(W))
ip_field.set('127.0.0.1')
ttk.Label(mainframe,text='Port: ',padding='5 0 0 0').grid(column=5,row=2,sticky=(W))
ttk.Entry(mainframe,textvariable=port_field,width=7).grid(column=6,row=2,sticky=(E))
port_field.set(4444)
ttk.Label(mainframe,text='',padding='0 0 15 15').grid(column=7,row=2)

connectButton = ttk.Button(mainframe, text="Connect", command=run, padding='0 2 0 2',width=30)
connectButton.grid(column=3, row=3, columnspan=2,sticky=(N))

statusLabel = ttk.Label(mainframe,textvariable=status)
statusLabel.grid(column=3, row=4, columnspan=4,sticky=(W))

window.mainloop()
disconnect()