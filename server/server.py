import re

from dataclasses import dataclass, asdict, field
import json
import asyncio
from typing import Set, Union
import pathlib

import websockets
from websockets.server import WebSocketServerProtocol

from nicegui import app, ui
from fastapi.middleware.cors import CORSMiddleware


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

CONNECTIONS: Set[WebSocketServerProtocol] = set()
CONFIG = {}

@dataclass(kw_only=True)
class Event:
    pass


@dataclass(kw_only=True)
class TimerSetEvent(Event):
    isRunning: bool = None
    time: int = None


def broadcast_event(e: Event):
    websockets.broadcast(CONNECTIONS, json.dumps({
                                        "type": e.__class__.__name__,
                                        "payload": asdict(e)
                                    }))

def get_config_path():
    return pathlib.Path(__file__).parent.joinpath(pathlib.Path("../config/server.cfg"))


def load_config():
    global CONFIG
    with open(get_config_path()) as fp:
        CONFIG = json.load(fp)


def reset_timer():
    broadcast_event(TimerSetEvent(isRunning=False,
                                  time=1500))

def start_timer():
    broadcast_event(TimerSetEvent(isRunning=True))


def stop_timer():
    broadcast_event(TimerSetEvent(isRunning=False))


def set_timer(new_time: Union[str, int]):
    if type(new_time) is str:
        reg_res = re.search(r"^(\d+)(?::(\d{1,2}))?$", timer_field.value, re.I)
        if reg_res:
            if reg_res.group(2) == None:
                new_timer_value = int(reg_res.group(1))
            else:
                new_timer_value = int(reg_res.group(1)) * 60 + int(reg_res.group(2))
            
            broadcast_event(TimerSetEvent(isRunning=False, time=new_timer_value))
    
    elif type(new_time) is int:
        broadcast_event(TimerSetEvent(isRunning=False, time=new_time))


# REST API
@app.get('/config')
def get_config():
    return CONFIG


# UI DEFINITION
ui.label('REVISION 2024 - SHADER SHOWDOWN OVERLAY DASHBOARD')
ui.button('Reload config', on_click=lambda: ui.notify('Configuration reloaded'))

ui.button('Start timer', on_click=start_timer).props('flat')
ui.button('Stop timer', on_click=stop_timer).props('flat')
ui.button('Reset timer', on_click=reset_timer).props('flat')

timer_field = ui.input(label="Timer")

ui.button('Set timer', on_click=lambda: set_timer(timer_field.value)).props('flat')

with ui.row().classes('items-center'):
    connections_label = ui.label('0')
    ui.label('Connections')

ui.separator().classes('mt-6')

ui.label('incoming messages:')
messages = ui.column().classes('ml-4')


async def handle_connect(websocket: WebSocketServerProtocol):
    """Register the new websocket connection, handle incoming messages and remove the connection when it is closed."""
    try:
        CONNECTIONS.add(websocket)
        connections_label.text = len(CONNECTIONS)
        async for data in websocket:
            with messages:
                ui.label(str(data))
    finally:
        CONNECTIONS.remove(websocket)
        connections_label.text = len(CONNECTIONS)


async def start_websocket_server():
    async with websockets.serve(handle_connect, 'localhost', 6969):
        await asyncio.Future()


load_config()

# start the websocket server when NiceGUI server starts
app.on_startup(start_websocket_server)


ui.run(host="localhost")
