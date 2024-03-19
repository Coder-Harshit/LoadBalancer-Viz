import tkinter as tk
import random
import time
import threading
from queue import Queue

class Server:
    def __init__(self, server_id, capacity):
        self.server_id = server_id
        self.capacity = capacity
        self.current_load = 0
        self.lock = threading.Lock()  # Add a lock to ensure thread safety

class Client:
    def __init__(self, client_id):
        self.client_id = client_id

class LoadBalancerVisualizer:
    def __init__(self, master, num_servers, servers):
        self.master = master
        self.servers = servers
        self.clients = []
        self.queue = Queue()  # Queue for holding clients when all servers are at full capacity
        self.canvas = tk.Canvas(master, width=800, height=500)
        self.canvas.pack()
        self.client_status = {}  # Track client status (active or queued)
        self.draw_servers()

    def draw_servers(self):
        for server in self.servers:
            x = 100 + int(server.server_id[1:]) * 200
            y = 100
            self.canvas.create_rectangle(x-20, y-20, x+20, y+20, fill='blue')
            self.canvas.create_text(x, y-30, text=f'Server {server.server_id}')

    def draw_clients(self):
        for i, client in enumerate(self.clients):
            x = 50 + i * 100
            y = 400
            
            if client in self.client_status:
                status = self.client_status[client]
                fill_color = 'green' if status == 'active' else 'red'
                
                # Draw clients on the canvas with respective colors
                self.canvas.create_rectangle(x-20, y-20, x+20, y+20, fill=fill_color)
                self.canvas.create_text(x, y+30, text=f'Client {client.client_id}')

    def generate_request(self):
        client_id = len(self.clients) + 1
        new_client = Client(client_id)
        
        # Check if all servers are at full capacity
        if all(server.current_load >= server.capacity for server in self.servers):
            print(f"All servers are at full capacity. Client {client_id} is queued.")
            self.client_status[new_client] = 'queued'
            self.queue.put(new_client)
            self.update_visualization()
            return
        
        self.client_status[new_client] = 'active'
        threading.Thread(target=self.process_request, args=(new_client,)).start()

    def process_request(self, client):
        next_server = self.get_next_server()
        # processing_time = random.randint(1, 5)  # Simulate processing time
        processing_time = 5  # Simulate processing time
        time.sleep(processing_time)  # Simulate request processing time
        
        with next_server.lock:
            next_server.current_load += 1  # Update server load after processing
        
        print(f"Client {client.client_id} sent request to Server {next_server.server_id}.")
        print(f"Request from client {client.client_id} processed by Server {next_server.server_id}.")
        print(f"Server {next_server.server_id} load: {next_server.current_load}/{next_server.capacity}")
        print()
        
        with next_server.lock:
            next_server.current_load -= 1  # Update server load after processing
        
        # Remove client from the dictionary
        del self.client_status[client]
        self.update_visualization()

    def get_next_server(self):
        for server in self.servers:
            if server.current_load < server.capacity:
                return server

    def update_visualization(self):
        self.canvas.delete(tk.ALL)
        self.draw_servers()
        self.draw_clients()

def main():
    root = tk.Tk()
    root.title("Load Balancer Visualizer")

    servers = [
        Server("S1", 3),
        Server("S2", 2),
        Server("S3", 1)
    ]

    lbv = LoadBalancerVisualizer(root, num_servers=len(servers), servers=servers)

    generate_button = tk.Button(root, text="Generate Request", command=lbv.generate_request)
    generate_button.pack()

    root.mainloop()

if __name__ == "__main__":
    main()
