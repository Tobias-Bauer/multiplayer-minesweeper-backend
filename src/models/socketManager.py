from typing import List
from fastapi import WebSocket
from traceback import print_exc


class WebsocketManager:
    def __init__(self) -> None:
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        try:
            self.active_connections.remove(websocket)
        except Exception as e:
            print("Exception occured at line 15 in socketManager.py")
            print(e)
            print_exc()

    async def broadcast(self, message: dict = {}):
        for socket in self.active_connections:
            try:
                await socket.send_json(message)
            except Exception as e:
                print("Exception occured at line 22 in socketManager.py")
                print(e)
                print_exc()
