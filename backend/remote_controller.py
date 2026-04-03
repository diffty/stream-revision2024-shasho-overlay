import os
from dotenv import load_dotenv

load_dotenv()

from nicegui import app, ui
from obswebsocket import obsws, requests


obs_ws_port = os.environ.get("OBS_WS_PORT", None)
obs_ws_password = os.environ.get("OBS_WS_PASSWORD", None)

if obs_ws_port is None:
    print("WARNING: OBS_WS_PORT is not set!!")

if obs_ws_password is None:
    print("WARNING: OBS_WS_PASSWORD is not set!!")


obs = obsws(port=obs_ws_port, password=obs_ws_password)
obs.connect()

def on_main_scene():
    obs.call(requests.SetCurrentProgramScene(sceneName="MAIN_COMPETITION"))


def on_coder_scene(coder_id: int, suffix: str = None):
    if suffix:
        suffix = f"_{suffix.upper()}"
    else:
        suffix = f""
        
    obs.call(requests.SetCurrentProgramScene(
        sceneName=f"CODER{coder_id}_ONLY{suffix}"
    ))


def on_code_toggle():
    pass


@ui.page('/')
def root_page():
    ui.tab_panel
    ui.label('EMERGENCY REMOTE CONTROLLER')

    ui.button("MAIN", on_click=on_main_scene)
    ui.separator()
    ui.button("CODER 1 WITH CAM", on_click=lambda: on_coder_scene(1, suffix="WITHCAM"))
    ui.button("CODER 2 WITH CAM", on_click=lambda: on_coder_scene(2, suffix="WITHCAM"))
    ui.button("CODER 3 WITH CAM", on_click=lambda: on_coder_scene(3, suffix="WITHCAM"))
    ui.separator()
    ui.button("TOGGLE CODE", on_click=on_code_toggle)
    ui.separator()
    ui.button("CODER 1 NO CAM", on_click=lambda: on_coder_scene(1))
    ui.button("CODER 2 NO CAM", on_click=lambda: on_coder_scene(2))
    ui.button("CODER 3 NO CAM", on_click=lambda: on_coder_scene(3))
    ui.separator()
    ui.button("CODER 1 SOLO", on_click=lambda: on_coder_scene(1, suffix="SOLO"))
    ui.button("CODER 2 SOLO", on_click=lambda: on_coder_scene(2, suffix="SOLO"))
    ui.button("CODER 3 SOLO", on_click=lambda: on_coder_scene(3, suffix="SOLO"))

ui.run(port=1991)
