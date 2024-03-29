<script setup lang="ts">
    import { ref } from 'vue';
    import OBSWebSocket from 'obs-websocket-js';

    const OBS_WS_ADDRESS = "ws://localhost:4455";
    const SERVER_WS_ADDRESS = "ws://localhost:6969";
    const SERVER_API_ADDRESS = "http://localhost:8080";
    const OBS_WS_PASSWORD = "meubapelefoute";

    var isObsConnected = false;
    var isServerConnected = false;

    // defineProps<{ nick: string }>()

    type Round = {
        coders: Array[string];
        djName: string;
        commentsName: string;
    }

    type Config = {
        roundName: string;
        hostName: string;
        round: Round;
    };

    const infoStripText = ref("")
    const sidePanelsVisibility = ref(true)
    const timerIsBig = ref(true)
    const isBottomInfoStripVisible = ref(false)
    const isBottomInfoStripTransitionActive = ref(false)
    const isTimerBlinking = ref(false);
    const isTimerColorsInverted = ref(false);
    const coderName1 = ref("");
    const coderName2 = ref("");
    const coderName3 = ref("");
    const currCoderName = ref("");
    const roundName = ref("");
    const djName = ref("");
    const commentsName = ref("");
    const hostName = ref("");
    const timer = ref(0);

    var timerState = {
        isRunning: false,
        startTime: -1,
        startState: 0
    }

    var config: Config;

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

    function toggleSidePanelsVisibility() {
        sidePanelsVisibility.value = !sidePanelsVisibility.value;
    }

    function toggleTimerSize() {
        timerIsBig.value = !timerIsBig.value;
    }

    function toggleBottomInfoStripVisibility() {
        isBottomInfoStripVisible.value = !isBottomInfoStripVisible.value;
        isBottomInfoStripTransitionActive.value = true;
    }

    function updateValuesUsingSceneName(sceneName: string) {
        if (sceneName == "MAIN_COMPETITION") {
            timerIsBig.value = true;
            sidePanelsVisibility.value = true;
            isBottomInfoStripVisible.value = false;
        }
        else {
            timerIsBig.value = false;
            sidePanelsVisibility.value = false;
            isBottomInfoStripVisible.value = true;
            
            const r = /CODER(\d+)/;
            var r_res = r.exec(sceneName);
            if (r_res != null) {
                const coderId = Number(r_res[1]) - 1;
                currCoderName.value = config.round.coders[coderId];
                infoStripText.value = config.round.coders[coderId];
            }
        }
    }

    // Timer callbacks
    var timerInterval: Timer | null = null;

    function updateTimerFromState() {
        if (timerState.isRunning) {
            const newTimerValue = (timerState.startState - (Date.now() - timerState.startTime) / 1000);
            timer.value = Math.max(newTimerValue, 0);
        }
        else {
            timer.value = timerState.startState;
        }
        
        // dashWs.send("test");
    }

    function updateTimerStyle() {
        // TODO: make timer blink when 0
        if (timer.value <= 10 && timer.value > 0) {
            isTimerBlinking.value = true;
        }
        else {
            isTimerBlinking.value = false;
        }
    }
    

    function timerCallback() {
        if (!timerState.isRunning && timerInterval != null) {
            clearInterval(timerInterval);
        }

        updateTimerFromState();
        updateTimerStyle();

    }
    
    // Dashboard connection and event handling
    const dashWs = new WebSocket(SERVER_WS_ADDRESS);
    // isTimerColorsInverted.value = true;

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
            case "TimerSetEvent":
                console.log(eventMsg);

                if (eventMsg.payload.time != null) {
                    //timer.value = eventMsg.payload.time;
                    timerState.startState = eventMsg.payload.time;
                }
                else {
                    timerState.startState = timer.value;
                }
                
                if (eventMsg.payload.isRunning == true && timerState.isRunning != true) {
                    timerState.isRunning = true;
                    timerState.startTime = Date.now();
                    window.setInterval(timerCallback, 200);
                }
                else {
                    timerState.isRunning = false;
                }

                updateTimerFromState();
                break
            
            case "ConfigEvent":
                if (eventMsg.payload.doUpdate) {
                    updateConfig();
                }

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
</script>

<template>
    <div class="side-panel" id="side-left-title" :class="{
        make_grow_side_panel: sidePanelsVisibility,
        make_shrink_side_panel: !sidePanelsVisibility }">

        <div style="margin: 20px; margin-top: 10px;">ROUND</div>

        <div class="side-panel-content" id="side-left-content" :class="{
            make_grow_side_panel_content: sidePanelsVisibility,
            make_shrink_side_panel_content: !sidePanelsVisibility }">

            <div style="margin: 20px; margin-top: 10px; color: black;">{{ roundName.toUpperCase() }}</div>
        </div>

        <div class="side-panel-shutter" id="side-left-shutter"></div>
    </div>
    
    <div class="side-panel" id="side-right-title" :class="{
        make_grow_side_panel: sidePanelsVisibility,
        make_shrink_side_panel: !sidePanelsVisibility }">

        <div style="margin: 20px; margin-top: 10px;">MUSIC</div>

        <div class="side-panel-content" id="side-right-content" :class="{
            make_grow_side_panel_content: sidePanelsVisibility,
            make_shrink_side_panel_content: !sidePanelsVisibility }">

            <div style="margin: 20px; margin-top: 10px; color: black;">{{ djName.toUpperCase() }}</div>
        </div>

        <div class="side-panel-shutter" id="side-right-shutter"></div>
    </div>

    <div id="container">
        <div id="bar-center" :class="{
            make_timer_small: !timerIsBig,
            make_timer_big: timerIsBig,
            invert: isTimerColorsInverted }">

            <div id="bar-bottom-info" :class="{
                    make_appear_bottom_infostrip: isBottomInfoStripVisible,
                    make_disappear_bottom_infostrip: !isBottomInfoStripVisible }">

                <div id="bar-bottom-info-left-edge">
                    <svg viewBox="0 0 100 100" preserveAspectRatio="none" style="right: 0;">
                        <polygon points="0,0 100,0 100,100" style="fill: black;"></polygon>
                    </svg>
                </div>

                <div id="bar-bottom-info-right-edge">
                    <svg viewBox="0 0 100 100" preserveAspectRatio="none" style="left: 0;">
                        <polygon points="0,0 100,0 0,100" style="fill: black;"></polygon>
                    </svg>
                </div>

                <Transition name="slide-right">
                    <div id="bar-bottom-info-text" :key="bar-bottom-info-text-content">
                        {{ infoStripText }}
                    </div>
                </Transition>
            </div>

            <div id="bar-left-edge">
                <svg viewBox="0 0 100 100" preserveAspectRatio="none" style="right: 0;">
                    <polygon points="0,0 100,0 100,100" style="fill: white;"></polygon>
                </svg>
            </div>

            <div id="bar-right-edge">
                <svg viewBox="0 0 100 100" preserveAspectRatio="none" style="left: 0;">
                    <polygon points="0,0 100,0 0,100" style="fill: white;"></polygon>
                </svg>
            </div>

            <div id="timer-text" :class="{ blink: isTimerBlinking }">{{ Math.floor(timer / 60).toString().padStart(2, '0') }}:{{ Math.floor(timer % 60).toString().padStart(2, '0') }}</div>
        </div>
    </div>

    <div id="coders-nameplates-container">
        <div class="coder-nameplate">{{ coderName1 }}</div>
        <div class="coder-nameplate">{{ coderName2 }}</div>
        <div class="coder-nameplate">{{ coderName3 }}</div>
    </div>

    <input type="text" id="bar-bottom-info-debug" v-model="infoStripText" style="position: absolute; bottom: 0px; left: 0%;"/>
    <button type="button" @click="toggleBottomInfoStripVisibility" style="position: absolute; bottom: 0px; left: 20%;">
        Toggle bottom info: {{ isBottomInfoStripVisible }}
    </button>
    <button type="button" @click="toggleSidePanelsVisibility" style="position: absolute; bottom: 0px; left: 40%;">
        Toggle edge: {{ sidePanelsVisibility }}
    </button>
    <button type="button" @click="toggleTimerSize" style="position: absolute; bottom: 0px; left: 60%;">
        Toggle timer: {{ timerIsBig }}
    </button>
</template>

<style scoped>
    @font-face {
        font-family: "Tungsten-Bold-TD";
        src: url("../assets/fonts/Tungsten-Bold-TD.woff") format("woff");
    }

    svg {
        width: 100%;
        height: 100%;
        position: absolute;
        bottom: 0;
    }
    
    button {
        font-size: 30px;
        width: 300px;
        height: 100px;
    }

    input {
        font-size: 30px;
        width: 300px;
        height: 100px;
    }


    #container {
        display: flex;
        /*overflow: hidden;*/
        white-space: nowrap;
        align-items: center;
        justify-content: center;
    }
    
    .side-panel {
        background-color: black;
        color: white;
        font-family: 'Tungsten-Bold-TD';
        font-size: 5em;
        line-height: 100%;
        overflow: hidden;
    }

    #side-left-title {
        position: fixed;
        right: 50%;
        top: 0;
        height: 100px;
    }

    #side-left-content {
        position: absolute;
        right: 0;
        top: 0;
        height: 100%;
        background-color: white;
    }

    #side-right-title {
        position: fixed;
        left: 50%;
        right: 0;
        top: 0;
        height: 100px;
        text-align: right;
    }

    #side-right-content {
        position: absolute;
        left: 0;
        top: 0;
        height: 100%;
        background-color: white;
    }

    #bar-left-edge, #bar-bottom-info-left-edge {
        position: absolute;
        width: 0.3em;
        height: 100%;
        top: 0;
        left: 0;
        margin-left: -0.3em;
    }

    #bar-right-edge, #bar-bottom-info-right-edge {
        position: absolute;
        width: 0.3em;
        height: 100%;
        top: 0;
        right: 0;
        margin-right: -0.3em;
    }

    #bar-bottom-info {
        position: absolute;
        background-color: black;
        left: 0.3em;
        right: 0.3em;
        height: 59px;
        /* margin-bottom: -0.35em; */
        bottom: 0em;
        z-index: -10;
    }

    #bar-bottom-info-text {
        color: white;
        font-size: 56px;
        line-height: 100%;
        height: 100%;
        text-align: center;
        overflow: hidden;
    }

    #bar-center {
        position: relative;
        font-family: 'Tungsten-Bold-TD';
        line-height: 100%;
        background-color: white;
        /*-webkit-text-stroke: 1px;
        -webkit-text-stroke-color: black;*/
        color: black;
        text-align: center;
    }

    .side-panel-shutter {
        position: absolute;
        height: 100%;
        background-color: black;
        top: 0;
        /* animation: 1s ease-in-out 0s shutter-animation infinite; */
    }

    #side-right-shutter {
        animation-direction: reverse;
    }

    @keyframes shutter-animation {
        0% {
            left: 0%;
            right: 100%;
        }
        50% {
            left: 0%;
            right: 0%;
        }
        100% {
            left: 100%;
            right: 0%;
        }
    }

    #timer-text {
        position: absolute;
        width: 100%;
    }

    #coders-nameplates-container {
        display: flex;
        flex-direction: column;
        position: absolute;
        bottom: 130px;
    }

    .coder-nameplate {
        background-color: white;
        color: black;
        font-family: 'Tungsten-Bold-TD';
        font-size: 5em;
        line-height: 100%;
        overflow: hidden;
        margin: 0.1em;
        width: 6em;
        padding: 0 0.1em 0 0.1em;
        text-align: center;
    }


    @keyframes blinker {
        50% {
            opacity: 0;
        }
    }

    .blink {
        animation: 0.5s blinker steps(1, end) infinite
    }

    .invert {
        filter: invert(1);
    }

    .make_grow_topbar {
        transition: width 0.50s;
        width: 100%;
    }

    .make_shrink_topbar {
        transition: width 0.50s;
        width: 550px;
    }

    .make_grow_side_panel {
        transition: width 0.50s;
        width: 50%;
    }

    .make_timer_small {
        transition: all 0.50s;
        height: 100px;
        width: 300px;
        font-size: 6.25em;
    }

    .make_timer_big {
        transition: all 0.50s;
        font-size: 15em;
        height: 250px;
        width: 500px;
    }

    .make_shrink_side_panel {
        transition: width 0.50s;
        width: 0%;
    }

    .make_grow_side_panel_content {
        transition: width 0.50s;
        transition-delay: 0.20s;
        width: 75%;
    }

    .make_shrink_side_panel_content {
        transition: width 0.50s;
        width: 0%;
    }

    .make_appear_bottom_infostrip {
        transition: margin-bottom 0.50s;
        margin-bottom: -59px;
    }

    .make_disappear_bottom_infostrip {
        transition: margin-bottom 0.50s;
        margin-bottom: 0px;
    }

    .slide-right-enter-active,
    .slide-right-leave-active {
        transition: all 0.5s ease;
        position: absolute;
        width: 100%;
    }

    .slide-right-enter-from {
        opacity: 0;
        margin-left: -100px;
    }
    .slide-right-enter-to,
    .slide-right-leave-from {
        opacity: 1;
        margin-left: 0px;
    }
    .slide-right-leave-to {
        opacity: 0;
        margin-left: 100px;
    }
</style>

