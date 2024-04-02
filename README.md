# Revision 2024 Shader Showdown Overlay

## Dependencies

* Environment
    * Python 3.11
        * NiceGUI
        * Websockets
    * bun
        * vite
        * vuejs

* OBS plugins:
    * [obs-composite-blur](https://obsproject.com/forum/resources/composite-blur.1780/)
    * [obs-move-transition](https://obsproject.com/forum/resources/move.913/)
    * [obs-transition-table](https://obsproject.com/forum/resources/transition-table.1174/)
    * [obs-stroke-glow-shadow](https://obsproject.com/forum/resources/stroke-glow-shadow.1800/)
    * OBS Websockets (should be intergated to OBS unless you installed it using a bad Arch Linux package for example)


## Installation

### Frontend

* Install `bun`
* Run `bun install` at the root of the repository


### Backend

* `cd backend`
* Activate the Python `virtualenv`
    * On Windows : `.venv/Scripts/Activate.bat`
    * On Linux/macOS : `source .venv/bin/activate`
* Run `pip install -r requirements.txt`


### OBS

* Import the scene collection `obs/Revision2024_ShaSho.json` in your OBS
* Make sure that the WebSockets server is enabled
    * Click on `Tools > WebSockets Server Settings`
    * Check `Enable WebSockets Server`
    * Enable authentification
    * Set `revision2024` as password (it can be customized at the top of `OverlayTop.vue` & `RevisionIntroSplash.vue`)
    * Apply


## Usage

### Backend

* Open a terminal at the repository root
* `cd backend`
* Activate the Python virtualenv
    * On Windows : `.venv/Scripts/Activate.bat`
    * On Linux/macOS : `source .venv/bin/activate`
* Run `python server.py`


### Frontend

#### For production

* Right after installing, you have to build at least once the frontend pages as static html using `bunx --bun vite build`.

Once successfully built, you can serve the `dist/` directory using the server of your choice, or access the frontend pages using the backend server that already serve them at these URLs:

* `http://localhost:8080/overlay/index.html`
* `http://localhost:8080/overlay/splash.html`


#### For testing/developing

* Open a terminal at the repository root
* Run `bunx --bun vite`

Overlay pages are now served by the bun/vite development server at the following URLs:
* `http://localhost:5173/index.html`
* `http://localhost:5173/splash.html`
