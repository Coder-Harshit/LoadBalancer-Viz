# importing libraries
import tkinter as tk
import random
import time
import threading

class Server:
    def __init__(self,serverId,capacity) -> None:
        self.serverId = serverId
        self.capacity = capacity
        self.currLoad = 0
        # Generate a random color for the server
        self.color = "#{:06x}".format(random.randint(0, 0xFFFFFF))
class Client:
    def __init__(self,clientId) -> None:
        self.clientId = clientId
class LoadBalancer:
    pass
class LoadBalancerVisualizer:
    def __init__(self,master,serverQuantity,servers,geometry) -> None:
        self.master = master
        self.servers = servers
        self.clients = []
        # print(geometry)
        self.frame = self.master
        # self.frame = tk.Frame(self.master)
        # self.frame.grid(row=0,column=0)
        # self.frame.config(width=geometry[0],height=geometry[1])
        # self.canvas = tk.Canvas(master,width=geometry[0],height=geometry[1])
        self.canvas = tk.Canvas(self.frame)
        self.scrollbar = tk.Scrollbar(self.frame,orient='horizontal',command=self.canvas.xview)
        self.genReqButton = tk.Button(self.frame,text="GENERATE REQ.", command=self.genReq)
        self.genReqButton.grid(row=2,column=0)
        self.canvas.config(xscrollcommand=self.scrollbar.set)
        # self.canvas.grid(row=0,column=0,columnspan=serverQuantity,padx=10,pady=10)
        self.canvas.grid(row=0,column=0,padx=10,pady=10,sticky='nsew')
        self.scrollbar.grid(row=1,column=0,sticky='ew')

        # Bind canvas to frame
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)
        self.canvas.bind("<Configure>", self.onCanvasConfigure)

        self.drawServers()
        # master.bind("<Configure>", self.onWindowResize)

    # def onWindowResize(self, event):
        # Adjust canvas size only if the user resizes the Tkinter window
        # if event.widget == self.master:
            # self.canvas.config(width=event.width)

        
    def onCanvasConfigure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def drawServers(self):
        for i,server in enumerate(self.servers):
            x = 100 + i*200
            y = 100
            serverText = f'{server.serverId}\nLoad: {server.currLoad}/{server.capacity}'
            server_rect = self.canvas.create_rectangle(x-40,y-40,x+40,y+40,fill='blue')
            server_text = self.canvas.create_text(x,y,text=serverText,justify=tk.CENTER,fill='white',tags=server.serverId)
            self.canvas.itemconfigure(server_text,tags=(server.serverId,))

    def genReq(self):
        clientId = len(self.clients)+1
        newClient = Client(clientId=clientId)
        self.clients.append(newClient)

         # Choose a server with available capacity
        available_servers = [server for server in self.servers if server.currLoad < server.capacity]
        if not available_servers:
            print("All servers are fully loaded")
            return
        server = random.choice(available_servers)

        # Update server load
        server.currLoad += 1

        # Draw line from client to server
        client_x = random.randint(50, self.canvas.winfo_width()-50)
        client_y = random.randint(200, self.canvas.winfo_height()-50)
        server_x = 100 + self.servers.index(server) * 200
        server_y = 100
        # color = "#{:06x}".format(random.randint(0, 0xFFFFFF))  # Random color for the line
        self.canvas.create_line(client_x, client_y, server_x, server_y, fill=server.color,width=3)

        # Draw client circle with its ID
        self.canvas.create_oval(client_x-20, client_y-20, client_x+20, client_y+20, fill='green')
        self.canvas.create_text(client_x, client_y, text=str(clientId), fill='white')

        # Update server load text
        serverText = f'{server.serverId}\nLoad: {server.currLoad}/{server.capacity}'
        print(serverText)
        print()
        self.canvas.itemconfigure(server.serverId, text=serverText)
        # print(self.canvas.itemconfigure(server.serverId, text="text"))



def main():
    root = tk.Tk()
    root.title("Load Balancer Visualizer")
    width = 600
    height = 500
    serverFarm = [
        Server("S1",1),
        Server("S2",2),
        Server("S3",3),
        # Server("S4",2),
        # Server("S5",2),
    ]
    root.geometry(f'{width}x{height}')
    lbv = LoadBalancerVisualizer(root,serverQuantity=len(serverFarm),servers=serverFarm,geometry=(width,height))
    root.mainloop()

if __name__=="__main__":
    main()