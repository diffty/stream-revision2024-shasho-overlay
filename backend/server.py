import re
import os

from dotenv import load_dotenv

from dataclasses import dataclass, asdict, field
import json
import time
import asyncio
from typing import Set, Union
import pathlib

import requests
import websockets
from websockets.server import WebSocketServerProtocol
from nicegui import app, ui
from fastapi.middleware.cors import CORSMiddleware


load_dotenv()


# CORS shit
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_static_files(url_path="/overlay", local_directory="./dist")


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


@dataclass(kw_only=True)
class UpdateResultsEvent(Event):
    coderRank1Name: str = ""
    coderRank2Name: str = ""
    coderRank3Name: str = ""
    coderRank1Votes: int = 0
    coderRank2Votes: int = 0
    coderRank3Votes: int = 0
    totalVotes: int = 0



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
PM_SHADER_TOKEN = os.environ.get("PM_SHADER_TOKEN", None)
PM_API_BASE_URL = os.environ.get("PM_API_BASE_URL", None)
PM_TEST_MODE = False
COMPETITIONS_EXPANSIONS_DICT = {}


if PM_SHADER_TOKEN is None:
    print("WARNING!! No PM_SHADER_TOKEN in env. Partymeister features will be unavailable!")


def broadcast_event(e: Event):
    # TODO: GET RID OF THIS ASAP PLEAAASSSE
    if isinstance(e, TimerSetEvent):
        if e.isRunning is not None:
            SERVER_TIMER_STATE.isRunning = e.isRunning

        if e.time is not None:
            SERVER_TIMER_STATE.time = e.time
        
    websockets.broadcast(
        CONNECTIONS,
        json.dumps({
            "type": e.__class__.__name__,
            "payload": asdict(e)
        })
    )

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
    global timer_field

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


@app.get('/competition_detail')
def get_pm_competition_detail(id: int):
    if PM_TEST_MODE:
        return {
            "data": {
                "id": 42,
                "name": "Shader Showdown Qualifier 1",
                "competition_type": "Shader Showdown",
                "sort_position": 10,
                "voting_enabled": True,
                "live_voting_enabled": False,
                "entries": [
                    {
                        "id": 101,
                        "title": "PlayerOne",
                        "author": "PlayerOne",
                        "sort_position": 1,
                        "status": 1,
                        "votes": 42.5
                    },
                    {
                        "id": 102,
                        "title": "PlayerTwo",
                        "author": "PlayerTwo",
                        "sort_position": 2,
                        "status": 1,
                        "votes": 38.0
                    }
                ],
                "total_votes": 80.5
            }
        }
    else:
        resp = requests.get(f"{PM_API_BASE_URL}/shader-showdown/competitions/{id}", headers={
            "X-Shader-Token": PM_SHADER_TOKEN,
        })
        return resp.json()


@app.get('/competitions_list')
def get_pm_competitions_list():
    global PM_TEST_MODE
    if PM_TEST_MODE:
        return {
            "data": [
                {
                    "id": 13,
                    "name": "Shader Showdown Round 1",
                    "competition_type": "Shader Showdown Final",
                    "sort_position": 100,
                    "voting_enabled": False,
                    "live_voting_enabled": False,
                    "entry_count": 0
                }
            ]
        }
    
    else:
        resp = requests.get(f"{PM_API_BASE_URL}/shader-showdown/competitions/", headers={
            "X-Shader-Token": PM_SHADER_TOKEN,
        })
        return resp.json()


def on_pm_api_test_change(new_state):
    global PM_TEST_MODE
    PM_TEST_MODE = new_state.value
    

def on_load_and_refresh_click():
    load_config_from_disk()
    broadcast_event(ConfigEvent(doUpdate=True))
    ui.notify('Loaded & refreshheeedd')


def on_load_config_from_disk_click():
    load_config_from_disk()
    ui.notify('Configuration reloaded from disk')


def on_refresh_overlay_config_click():
    broadcast_event(ConfigEvent(doUpdate=True))


def send_round_results_to_overlay(entries_data):
    coders_list = list(
        map(
            lambda e: (e["title"], e["votes"]),
            sorted(
                entries_data,
                key=lambda e: e["votes"],
                reverse=True
            )
        )
    )

    broadcast_event(
        UpdateResultsEvent(
            coderRank1Name=coders_list[0][0],
            coderRank2Name=coders_list[1][0],
            coderRank3Name=coders_list[2][0],
            coderRank1Votes=coders_list[0][1],
            coderRank2Votes=coders_list[1][1],
            coderRank3Votes=coders_list[2][1],
            totalVotes=0,
        )
    )


def refresh_single_competition_results(id: int):
    comp_detail = get_pm_competition_detail(id)

    if comp_detail and "data" in comp_detail:
        comp_data = comp_detail["data"]
        comp_exp = COMPETITIONS_EXPANSIONS_DICT[id]
        comp_exp.clear()
        
        with comp_exp:
            entries_data = comp_data["entries"]

            series = []

            entries_title_list = []
            entries_votes_list = []
            
            for entry_data in entries_data:
                entries_title_list.append(entry_data["title"])
                entries_votes_list.append(entry_data["votes"])

            series.append(
                {
                    'type': 'bar',
                    'data': entries_votes_list
                }
            )

            ui.echart({
                'xAxis': {'type': 'value'},
                'yAxis': {'type': 'category', 'data': entries_title_list, 'inverse': True},
                'legend': {'textStyle': {'color': 'gray'}},
                'series': series,
            })

            state_to_str = lambda state: "enabled" if state is True else "disabled"
            state_css_class = lambda state: "text-green-500" if state is True else "text-red-500"

            ui.button("Send round results to overlay", on_click=lambda: send_round_results_to_overlay(entries_data))
            
            ui.label(f"Voting is {state_to_str(comp_data['voting_enabled'])}").classes(state_css_class(comp_data['voting_enabled']))
            ui.label(f"Live voting is {state_to_str(comp_data['live_voting_enabled'])}").classes(state_css_class(comp_data['live_voting_enabled']))

    else:
        ui.label("Can't retrieve entry data!")


def on_refresh_opened_competitions():
    for comp_id, comp_exp in COMPETITIONS_EXPANSIONS_DICT.items():
        if comp_exp.value == True:
            refresh_single_competition_results(comp_id)


def on_refresh_results_click():
    global results_div

    results_div.clear()

    COMPETITIONS_EXPANSIONS_DICT.clear()

    comp_results_list = get_pm_competitions_list()

    with results_div:
        if comp_results_list and "data" in comp_results_list:
            for comp_result in comp_results_list["data"]:
                with ui.expansion(comp_result["name"]).classes('w-full') as comp_expansion:
                    COMPETITIONS_EXPANSIONS_DICT[comp_result["id"]] = comp_expansion
                    refresh_single_competition_results(comp_result["id"])
        else:
            ui.label("Competitions info loading failed!")


@ui.page('/')
def root_page():
    global connections_label, messages, timer_field, results_div
    
    # UI DEFINITION
    ui.label('REVISION 2026 - SHADER SHOWDOWN OVERLAY DASHBOARD')

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

    ui.label('Results')

    with ui.row():
        ui.button('Refetch All', on_click=on_refresh_results_click)
        ui.button('Refresh Opened', on_click=on_refresh_opened_competitions)

    results_div = ui.column().classes('ml-4')

    ui.checkbox("PM API TEST", on_change=on_pm_api_test_change)

    ui.separator().classes('mt-6')

    ui.label('incoming messages:')
    messages = ui.column().classes('ml-4')


async def handle_connect(websocket: WebSocketServerProtocol):
    """Register the new websocket connection, handle incoming messages and remove the connection when it is closed."""

    global connections_label, messages
    
    try:
        CONNECTIONS.add(websocket)
        connections_label.text = len(CONNECTIONS)
        async for data in websocket:
            with messages:
                ui.label(str(data))
    finally:
        CONNECTIONS.remove(websocket)
        connections_label.text = len(CONNECTIONS)


# start the websocket server when NiceGUI server starts
@app.on_startup
async def start_websocket_server():

    async with websockets.serve(handle_connect, 'localhost', 6969):
        await asyncio.Future()


load_config_from_disk()

SERVER_TIMER_STATE = TimerSetEvent(isRunning=False, time=CONFIG.roundDuration)



ui.run(host="0.0.0.0")
