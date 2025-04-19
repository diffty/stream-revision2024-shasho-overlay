<script setup lang="ts">
    import { ref } from 'vue';
    import OBSWebSocket from 'obs-websocket-js';
    import ScrollingTitle from './ScrollingTitle.vue'
    
    // CONSTANTS
    const OBS_WS_ADDRESS = "ws://localhost:4455";
    const SERVER_WS_ADDRESS = "ws://localhost:6969";
    const SERVER_API_ADDRESS = "http://localhost:8080";
    const OBS_WS_PASSWORD = "revision2024";

    // PROPS
    const currObsSceneName = ref("INTRO");

    // FLAGS
    var isObsConnected = false;
    var isServerConnected = false;


    // OBJECTS DEFINITIONS
    type Round = {
        coders: Array<string>;
        djName: string;
        commentsName: string;
    }

    type Config = {
        roundName: string;
        hostName: string;
        round: Round;
    };

    const coderName1 = ref("");
    const coderName2 = ref("");
    const coderName3 = ref("");
    const roundName = ref("");
    const djName = ref("");
    const commentsName = ref("");
    const hostName = ref("");

    const isOpened = ref(false)

    var config: Config;

    function updateValuesUsingSceneName(sceneName: string) {
        currObsSceneName.value = sceneName;
        isOpened.value = !(sceneName === 'INTRO');
    }

    async function updateConfig() {
        const configFile = await fetch(`${SERVER_API_ADDRESS}/current_round`)
                                    .catch((e: Error) => {
                                        console.error(`Can't retrieve current round infos : ${e}`)
                                    });

        if (configFile && configFile.status == 200) {
            console.log("Config loaded!")
            config = await configFile.json();

            coderName1.value = config.round.coders[0];
            coderName2.value = config.round.coders[1];
            coderName3.value = config.round.coders[2];
            roundName.value = config.roundName;
            djName.value = config.round.djName;
            commentsName.value = config.round.commentsName;
            hostName.value = config.hostName;
        }
    }

    // Dashboard connection and event handling
    const dashWs = new WebSocket(SERVER_WS_ADDRESS);

    dashWs.addEventListener("open", () => {
        console.log(`Connected to server ${SERVER_WS_ADDRESS}.`);
        isServerConnected = true;
    });

    dashWs.addEventListener("error", (ev: ErrorEvent) => {
        console.error(`Error with the server Websocket connection ${SERVER_WS_ADDRESS}`);
        isServerConnected = false;
    });

    dashWs.addEventListener("close", (e: CloseEvent) => {
        console.error(`Websocket connection with server ${SERVER_WS_ADDRESS} closed.`);
        isServerConnected = false;
    });

    dashWs.addEventListener("message", (e: MessageEvent) => {
        const eventMsg = JSON.parse(e.data);

        switch (eventMsg.type) {
            case "ConfigEvent":
                if (eventMsg.payload.doUpdate) {
                    updateConfig();
                }
                break;
        }
    })

    // OBS connection
    const obs = new OBSWebSocket();
    await obs.connect(OBS_WS_ADDRESS, OBS_WS_PASSWORD)
                    .then(() => {
                        isObsConnected = true;
                    })
                    .catch(() => {
                        console.error(`Can't connect to OBS websockets ${OBS_WS_ADDRESS}`);
                    });

    obs.on("SceneTransitionStarted", async function (evt: object) {
        const nextSceneInfo = await obs.call("GetCurrentProgramScene");
        updateValuesUsingSceneName(nextSceneInfo.currentProgramSceneName);
    });

    obs.on("ConnectionError", () => {
        isObsConnected = false;
    });

    obs.on("ConnectionClosed", () => {
        isObsConnected = false;
    });

    await updateConfig();

    if (isObsConnected) {
        const currObsSceneInfo = await obs.call("GetCurrentProgramScene");
        updateValuesUsingSceneName(currObsSceneInfo.sceneName);
    }

    function toggleOpen() {
        console.log(isOpened.value);
        isOpened.value = !isOpened.value;
    }
</script>

<template>
    <div id="whole-title">
        <div id="bottom-line">
            <div id="round" class="medium-text"><span class="cell-title">{{ roundName }}</span></div>
            <div id="dj-text" class="medium-text"><span class="cell-title">DJ</span><span class="cell-content">{{ djName }}</span></div>
            <div id="comments-text" class="medium-text"><span class="cell-title">COMMENTS</span><span class="cell-content">{{ commentsName }}</span></div>
            <!-- <div id="host-text" class="tiny-text">and tech from {{ hostName }}</div> -->
        </div>

        <div id="middle-line">
            <div id="coder1" class="coder">{{ coderName1 }}</div>
            <span class="vs">VS</span>
            <div id="coder2" class="coder">{{ coderName2 }}</div>
            <span class="vs">VS</span>
            <div id="coder3" class="coder">{{ coderName3 }}</div>
        </div>

        <div class="top-part" :class="{ do_open: isOpened, do_close: !isOpened, do_shrink: isOpened, do_grow: !isOpened }">
            <ScrollingTitle text="SHADER" id="title-scrolling-shader" animDuration="10s" class="title-scrolling" />
        </div>

        <div class="bottom-part" :class="{ do_open: isOpened, do_close: !isOpened, do_shrink: isOpened, do_grow: !isOpened }">
            <ScrollingTitle text="SHOWDOWN" reversed id="title-scrolling-showdown" animDuration="10s" class="title-scrolling" />
        </div>
    </div>
    <!-- <button type="button" @click="toggleOpen" style="position: absolute; bottom: 0px; left: 60%;">
        Open it
    </button> -->
</template>

<style scoped>
    @font-face {
        font-family: "Tungsten-Bold-TD";
        src: url("./assets/fonts/Tungsten-Bold-TD.woff") format("woff");
        font-weight: normal;
        font-style: normal;
    }

    .cell-title {
        background-color: black;
        color: white;
        font-weight: bold;
        padding: 10px;
    }

    .cell-content {
        background-color: white;
        color: black;
        padding: 10px;
    }

    .big-text {
        font-family: "Chivo", sans-serif;
        font-size: 5em;
        text-align: center;
    }

    .medium-text {
        font-family: "Chivo", sans-serif;
        font-size: 3em;
        text-align: center;
    }

    .tiny-text {
        font-family: "Chivo", sans-serif;
        font-size: 1em;
        text-align: center;
    }

    #round {
        display: inline;
    }

    #round .cell-title {
        padding-left: 20px;
        padding-right: 20px;
    }

    #middle-line {
        position: absolute;
        bottom: 25%;
        width: 100%;
        text-align: center;
    }

    #bottom-line {
        position: absolute;
        bottom: 17.75%;
        width: 100%;
        text-align: center;
    }

    #dj-text {
        display: inline;
        margin-left: 20px;
    }

    #comments-text {
        display: inline;
        margin-left: 20px;
    }

    #host-text {
        position: absolute;
        left: 65%;
    }

    .vs {
        font-family: "Chivo", sans-serif;
        font-size: 3em;
        font-weight: bold;
        text-align: center;
        background-color: black;
        color:white;
        padding-left: 10px;
        padding-right: 10px;
        margin: 10px;
    }

    .coder {
        font-family: "Chivo", sans-serif;
        font-size: 5em;
        font-weight: bold;
        text-align: center;
        background-color: white;
        padding-left: 20px;
        padding-right: 20px;
    }

    #coder1 {
        display: inline;
    }

    #coder2 {
        display: inline;
    }

    #coder3 {
        display: inline;
    }

    #whole-title {
        position: absolute;
        display: block;
        width: 100%;
        height: 100%;
        transform: rotate(-5deg) scale(1.15);
    }

    .do_open {
        transition: height 0.5s, font-size 0.5s;
        height: 16%;
        font-size: 15em;
    }

    .do_close {
        transition: height 0.5s, font-size 0.5s;
        height: 50%;
        font-size: 15em;
    }

    .top-part {
        display: block;
        /* height: 50%; */
        width: 100%;
        position: absolute;
        top: 0px;
        background-color: white;
    }

    .bottom-part {
        display: block;
        /* height: 50%; */
        width: 100%;
        position: absolute;
        bottom: 0px;
        background-color: black;
    }

    .title-scrolling {
        display: block;
        position: absolute;

        height: 250px;
        
        font-family: "Chivo", sans-serif;
        font-optical-sizing: auto;
        font-weight: 800;
        font-style: italic;
        text-align: center;
    }

    #title-scrolling-shader {
        bottom: 0%;
        width: 100%;

        color: black;
    }

    #title-scrolling-showdown {
        top: 0%;
        width: 100%;

        color: white;
    }
</style>
