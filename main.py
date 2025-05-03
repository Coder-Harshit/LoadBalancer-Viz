import sys
import random
import time
from PySide6.QtCore import Qt, Signal, QThread, QRectF
from PySide6.QtGui import QPen, QColor
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton,
    QGraphicsView, QGraphicsScene, QGraphicsRectItem,
    QGraphicsEllipseItem, QGraphicsLineItem, QGraphicsTextItem
)

class Server:
    def __init__(self, server_id, capacity):
        self.server_id = server_id
        self.capacity = capacity
        self.curr_load = 0
        self.color = QColor(Qt.blue)

class Client:
    def __init__(self, client_id):
        self.client_id = client_id

class RequestWorker(QThread):
    finished_signal = Signal(object, object, object)

    def __init__(self, client, server, parent=None):
        super().__init__(parent)
        self.client = client
        self.server = server

    def run(self):
        processing_time = random.randint(1, 7)
        time.sleep(processing_time)
        self.server.curr_load -= 1
        self.finished_signal.emit(self, self.client, self.server)

class LoadBalancerVisualizer(QWidget):
    def __init__(self, servers):
        super().__init__()
        self.setWindowTitle("Load Balancer Visualizer - PySide6")
        self.servers = servers
        self.clients_items = {}
        self.workers = []  # keep references to threads
        self.client_count = 0

        layout = QVBoxLayout(self)
        self.button = QPushButton("Generate Request")
        self.button.clicked.connect(self.generate_request)
        layout.addWidget(self.button)

        self.view = QGraphicsView()
        self.scene = QGraphicsScene(self)
        self.view.setScene(self.scene)
        layout.addWidget(self.view)

        self.draw_servers()
        self.resize(800, 600)

    def draw_servers(self):
        spacing = 200
        y = 100
        size = 80
        pen = QPen(QColor(Qt.black))
        for i, server in enumerate(self.servers):
            x = 100 + i * spacing
            rect = QGraphicsRectItem(QRectF(x - size/2, y - size/2, size, size))
            rect.setBrush(server.color)
            rect.setPen(pen)
            self.scene.addItem(rect)
            text = QGraphicsTextItem(f"{server.server_id}\n{server.curr_load}/{server.capacity}")
            text.setDefaultTextColor(QColor(Qt.white))
            text.setPos(x - size/4, y - size/4)
            self.scene.addItem(text)
            server._graphic = {'rect': rect, 'text': text, 'pos': (x, y)}

    def update_server_graphic(self, server):
        gfx = server._graphic
        gfx['text'].setPlainText(f"{server.server_id}\n{server.curr_load}/{server.capacity}")

    def generate_request(self):
        self.client_count += 1
        client = Client(self.client_count)
        available = [s for s in self.servers if s.curr_load < s.capacity]
        if not available:
            print("All servers are fully loaded")
            return
        server = random.choice(available)
        server.curr_load += 1
        self.update_server_graphic(server)

        view_width = int(self.view.viewport().width())
        view_height = int(self.view.viewport().height())
        x = random.randint(50, max(50, view_width - 50))
        y = random.randint(200, max(200, view_height - 50))

        circle = QGraphicsEllipseItem(x - 20, y - 20, 40, 40)
        circle.setBrush(QColor(Qt.green))
        circle.setPen(QPen(Qt.NoPen))
        self.scene.addItem(circle)
        client_text = QGraphicsTextItem(str(client.client_id))
        client_text.setDefaultTextColor(QColor(Qt.white))
        client_text.setPos(x - 5, y - 10)
        self.scene.addItem(client_text)

        sx, sy = server._graphic['pos']
        line = QGraphicsLineItem(x, y, sx, sy)
        line.setPen(QPen(server.color))
        self.scene.addItem(line)

        self.clients_items[client] = (circle, client_text, line)

        worker = RequestWorker(client, server, parent=self)
        worker.finished_signal.connect(self.on_request_finished)
        worker.finished_signal.connect(self.cleanup_worker)
        self.workers.append(worker)
        worker.start()

    def on_request_finished(self, worker, client, server):
        self.update_server_graphic(server)
        items = self.clients_items.pop(client, None)
        if items:
            for item in items:
                self.scene.removeItem(item)

    def cleanup_worker(self, worker, client, server):
        # Remove finished thread references
        try:
            self.workers.remove(worker)
        except ValueError:
            pass
        worker.deleteLater()

    def closeEvent(self, event):
        # Wait for all threads to finish
        for worker in list(self.workers):
            worker.wait()
        super().closeEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    servers = [Server(f"S{i+1}", cap) for i, cap in enumerate([1, 2, 3])]
    window = LoadBalancerVisualizer(servers)
    window.show()
    sys.exit(app.exec())
