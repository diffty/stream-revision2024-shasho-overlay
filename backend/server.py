import re

from dataclasses import dataclass, asdict, field
import json
import time
import asyncio
from typing import Set, Union
import pathlib

import websockets
from websockets.server import WebSocketServerProtocol

from nicegui import app, ui
from fastapi.middleware.cors import CORSMiddleware


# CORS shit
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_static_files(url_path="/overlay", local_directory="../dist")


@dataclass(kw_only=True)
class Event:
    pass


@dataclass(kw_only=True)
class TimerSetEvent(Event):
    isRunning: bool = None
    time: int = None
    startTime: float = None



@dataclass(kw_only=True)
class ConfigEvent(Event):
    doUpdate: bool = False


@dataclass
class Round:
    coders: list[str]
    djName: str
    commentsName: str


@dataclass()
class Config:
    roundName: str
    currRoundId: int
    rounds: list[Round]
    hostName: str
    roundDuration: int


CONNECTIONS: Set[WebSocketServerProtocol] = set()
CONFIG = None
SERVER_TIMER_STATE = None


def broadcast_event(e: Event):
    # TODO: GET RID OF THIS ASAP PLEAAASSSE
    if isinstance(e, TimerSetEvent):
        if e.isRunning is not None:
            SERVER_TIMER_STATE.isRunning = e.isRunning

        if e.time is not None:
            SERVER_TIMER_STATE.time = e.time
        
    websockets.broadcast(CONNECTIONS, json.dumps({
                                        "type": e.__class__.__name__,
                                        "payload": asdict(e)
                                    }))

def get_config_path():
    return pathlib.Path(__file__).parent.joinpath(pathlib.Path("../config/server.cfg"))


def load_config_from_disk():
    global CONFIG
    with open(get_config_path()) as fp:
        config_json = json.load(fp)
        CONFIG = Config(**config_json)
        

def reset_timer():
    broadcast_event(TimerSetEvent(isRunning=False,
                                  time=1500))


def start_timer():
    broadcast_event(TimerSetEvent(isRunning=True))
    SERVER_TIMER_STATE.startTime = time.time()


def pause_timer():
    broadcast_event(TimerSetEvent(isRunning=False))


def set_timer(new_time: Union[str, int]):
    if type(new_time) is str:
        reg_res = re.search(r"^(\d+)(?::(\d{1,2}))?$", timer_field.value, re.I)
        if reg_res:
            if reg_res.group(2) == None:
                new_timer_value = int(reg_res.group(1))
            else:
                new_timer_value = int(reg_res.group(1)) * 60 + int(reg_res.group(2))
            
            broadcast_event(TimerSetEvent(time=new_timer_value))
    
    elif type(new_time) is int:
        broadcast_event(TimerSetEvent(time=new_time))
    
    # Updating it in server state just in case
    SERVER_TIMER_STATE.startTime = time.time()


# REST API
@app.get('/current_round')
def get_current_round():
    curr_round_infos = CONFIG.rounds[CONFIG.currRoundId]

    return {
        "roundName": CONFIG.roundName,
        "hostName": CONFIG.hostName,
        "round": curr_round_infos,
    }


@app.get('/timer')
def get_timer_state():
    return {
        "isRunning": SERVER_TIMER_STATE.isRunning,
        "time": SERVER_TIMER_STATE.time,
        "startTime": SERVER_TIMER_STATE.startTime,
    }


def on_load_and_refresh_click():
    load_config_from_disk()
    broadcast_event(ConfigEvent(doUpdate=True))
    ui.notify('Loaded & refreshheeedd')


def on_load_config_from_disk_click():
    load_config_from_disk()
    ui.notify('Configuration reloaded from disk')


def on_refresh_overlay_config_click():
    broadcast_event(ConfigEvent(doUpdate=True))


# UI DEFINITION
ui.label('REVISION 2025 - SHADER SHOWDOWN OVERLAY DASHBOARD')

ui.button('Load & Refresh', on_click=on_load_and_refresh_click)
ui.button('Load config from disk', on_click=on_load_config_from_disk_click)
ui.button('Refresh overlay config', on_click=on_refresh_overlay_config_click)

ui.button('Start timer', on_click=start_timer)
ui.button('Pause timer', on_click=pause_timer)
ui.button('Reset timer', on_click=reset_timer)

timer_field = ui.input(label="Timer", value="25:00")

ui.button('Set timer', on_click=lambda: set_timer(timer_field.value))


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


load_config_from_disk()

SERVER_TIMER_STATE = TimerSetEvent(isRunning=False, time=CONFIG.roundDuration)

# start the websocket server when NiceGUI server starts
app.on_startup(start_websocket_server)


ui.run(host="0.0.0.0")
