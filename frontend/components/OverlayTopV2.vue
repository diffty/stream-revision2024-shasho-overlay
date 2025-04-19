<script setup lang="ts">
    import { ref } from 'vue';
    import OBSWebSocket from 'obs-websocket-js';
    import ScrollingTitle from './ScrollingTitle.vue';
    import DigitWheel from './DigitWheel.vue';
    import SidebarScrollingTitle from './SidebarScrollingTitle.vue';

    const OBS_WS_ADDRESS = "ws://localhost:4455";
    const SERVER_WS_ADDRESS = "ws://localhost:6969";
    const SERVER_API_ADDRESS = "http://localhost:8080";
    const OBS_WS_PASSWORD = "revision2024";

    var isObsConnected = false;
    var isServerConnected = false;

    // defineProps<{ nick: string }>()

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

    const infoStripText = ref("")
    const sidePanelsVisibility = ref(1)
    const sidePanelsContentVisibility = ref(1)
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
    const sidebar_left_title = ref("ROUND")
    const sidebar_left_content = ref("")
    const sidebar_right_title = ref("MUSIC")
    const sidebar_right_content = ref("")
    const shutter_left = ref();
    const shutter_right = ref();
    const side_left_content = ref();
    const side_right_content = ref();

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

    async function pullTimer() {
        const timerStateInfoRequest = await fetch(`${SERVER_API_ADDRESS}/timer`)
                                    .catch((e: Error) => {
                                        console.error(`Can't retrieve current timer infos : ${e}`)
                                    });

        if (timerStateInfoRequest && timerStateInfoRequest.status == 200) {
            console.log("Timer loaded!")
            let timerStateInfo = await timerStateInfoRequest.json();
            
            timerState.isRunning = timerStateInfo.isRunning;
            timerState.startTime = timerStateInfo.startTime * 1000;
            timerState.startState = timerStateInfo.time;

            console.log(timerState);

            if (timerState.isRunning) {
                if (timerInterval != null) {
                    clearInterval(timerInterval);
                    timerInterval = null;
                }
                timerInterval = window.setInterval(timerCallback, 200);
            }
            
            updateTimerFromState();
        }
    }

    function toggleSidePanelsVisibility() {
        sidePanelsVisibility.value = sidePanelsVisibility.value == 0 ? 1 : 0;
        //sidePanelsContentVisibility.value = sidePanelsContentVisibility.value == 0 ? 1 : 0;
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
            sidePanelsVisibility.value = 1;
            sidePanelsContentVisibility.value = 1;
            isBottomInfoStripVisible.value = false;
        }
        else {
            timerIsBig.value = false;
            sidePanelsVisibility.value = 0;
            sidePanelsContentVisibility.value = 0;
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
    var timerInterval: number | null = null;

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
            timerInterval = null;
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

                if (eventMsg.payload.time != null && eventMsg.payload.time != undefined) {
                    //timer.value = eventMsg.payload.time;
                    timerState.startState = eventMsg.payload.time;
                }
                else {
                    timerState.startState = timer.value;
                }
                
                timerState.startTime = Date.now();

                if (eventMsg.payload.isRunning == true && timerState.isRunning != true) {
                    if (timerInterval != null) {
                        clearInterval(timerInterval);
                        timerInterval = null;
                    }

                    timerInterval = window.setInterval(timerCallback, 200);
                }
                
                if (eventMsg.payload.isRunning != null && eventMsg.payload.isRunning != undefined) {
                    timerState.isRunning = eventMsg.payload.isRunning;
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
    await pullTimer();

    if (isObsConnected) {
        const currObsSceneInfo = await obs.call("GetCurrentProgramScene");
        updateValuesUsingSceneName(currObsSceneInfo.sceneName);
    }

    sidebar_left_content.value = roundName.value
    sidebar_right_content.value = djName.value

    function animate() {
        shutter_left.value.classList.add("shutter-activated")
        sidebar_left_title.value = ""

        shutter_right.value.classList.add("shutter-activated")
        sidebar_right_title.value = ""

        window.setTimeout(() => {
            sidePanelsContentVisibility.value = 2;
        }, 500)

        shutter_left.value.addEventListener("animationend", (e: any) => {
            shutter_left.value.classList.remove("shutter-activated");

            if (sidebar_left_title.value == "ROUND") {
                sidebar_left_title.value = "COMMENTS"
                sidebar_left_content.value = commentsName.value
            }
            else {
                sidebar_left_title.value = "ROUND"
                sidebar_left_content.value = roundName.value
            }

            sidePanelsContentVisibility.value = 1;
        })

        shutter_right.value.addEventListener("animationend", (e: any) => {
            shutter_right.value.classList.remove("shutter-activated");

            if (sidebar_right_title.value == "MUSIC") {
                sidebar_right_title.value = "VJING"
                sidebar_right_content.value = hostName.value
            }
            else {
                sidebar_right_title.value = "MUSIC"
                sidebar_right_content.value = djName.value
            }

            sidePanelsContentVisibility.value = 1;
        })

        setTimeout(animate, 20000);
    }

    setTimeout(animate, 20000);
</script>

<template>
    <div class="side-panel" id="side-left-title" :class="{
        make_grow_side_panel: sidePanelsVisibility == 1,
        make_shrink_side_panel: sidePanelsVisibility == 0 }">

        <div class="sidebar">
            <div style="position: absolute; left: 20px; width: 100%;">
                <SidebarScrollingTitle :text="sidebar_left_title" />
            </div>
        </div>

        <div ref="side_left_content" class="side-panel-content" id="side-left-content" :class="{
            make_grow_side_panel_content: sidePanelsContentVisibility == 1,
            make_shrink_side_panel_content: sidePanelsContentVisibility == 0,
            make_instant_open_side_panel_content: sidePanelsContentVisibility == 2 }">

            <div style="margin: 20px; margin-top: 10px; color: black;">{{ sidebar_left_content.toUpperCase() }}</div>
        </div>
        
        <div ref="shutter_left" class="side-panel-shutter" id="side-left-shutter"></div>
    </div>
    
    <div class="side-panel" id="side-right-title" :class="{
        make_grow_side_panel: sidePanelsVisibility == 1,
        make_shrink_side_panel: sidePanelsVisibility == 0 }">

        <div class="sidebar">
            <div style="position: absolute; right: 20px; width: 100%;">
                <SidebarScrollingTitle :text="sidebar_right_title" side="right" />
            </div>
        </div>

        <div ref="side_right_content" class="side-panel-content" id="side-right-content" :class="{
            make_grow_side_panel_content: sidePanelsContentVisibility == 1,
            make_shrink_side_panel_content: sidePanelsContentVisibility == 0,
            make_instant_open_side_panel_content: sidePanelsContentVisibility == 2 }">

            <div style="margin: 20px; margin-top: 10px; color: black;">{{ sidebar_right_content.toUpperCase() }}</div>
        </div>

        <div ref="shutter_right" class="side-panel-shutter" id="side-right-shutter"></div>
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

            <div id="timer-text" :class="{ blink: isTimerBlinking }">
                <DigitWheel :num="Math.floor(timer / 60).toString().padStart(2, '0')[0]"/>
                <DigitWheel :num="Math.floor(timer / 60).toString().padStart(2, '0')[1]"/>
                <div class="timer-digit-wrap">
                    <div class="timer-digit-container" style="width: 0.40ch">
                        <span class="timer-digit" style="width: auto">:</span>
                    </div>
                </div>
                <DigitWheel :num="Math.floor(timer % 60).toString().padStart(2, '0')[0]"/>
                <DigitWheel :num="Math.floor(timer % 60).toString().padStart(2, '0')[1]"/>
            </div>
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
        Toggle edge: {{ sidePanelsVisibility }} / {{ sidePanelsContentVisibility }}
    </button>
    <button type="button" @click="toggleTimerSize" style="position: absolute; bottom: 0px; left: 60%;">
        Toggle timer: {{ timerIsBig }}
    </button>
</template>

<style> 
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

    .sidebar {
        margin: 20px;
        margin-top: 10px;
        width: 100%;
    }

    #side-left-title {
        position: fixed;
        right: 50%;
        top: 0;
        height: 100px;
    }

    #side-left-content {
        position: absolute;
        /* right: 0; */
        left: 32%;
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
        right: 32%;
        top: 0;
        height: 100%;
        background-color: white;
    }

    .side-panel-content {
        overflow: hidden;
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

    /* SHUTTER */
    .side-panel-shutter {
        position: absolute;
        height: 100%;
        background-color: black;
        top: 0;
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
        90% {
            left: 0%;
            right: 0%;
        }
        100% {
            left: 100%;
            right: 0%;
        }
    }

    .shutter-activated {
        animation: 0.9s ease-in-out 0s shutter-animation 1;
    }

    /* TIMER */
    #timer-text {
        position: absolute;
        width: 100%;
        height: 100%;
        overflow: hidden;
    }

    .timer-digit-wrap {
        display: inline-block;
   }

    .timer-digit-container {
        transform-style: preserve-3d;
        height: 1em;
        width: 1ch;
    }

    .timer-digit {
        line-height: 1;
        backface-visibility: hidden;
        position: absolute;
        top: 0;
        left: 0;
        width: 1ch;

    }
    
    @keyframes blinker {
        50% {
            opacity: 0;
        }
    }

    .blink {
        animation: 0.5s blinker steps(1, end) infinite
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

    .instant_close_side_panel_content {
        transition: width 1ms;
        width: 0%;
    }

    .make_timer_small {
        transition: all 0.50s;
        height: 100px;
        width: 300px;
        font-size: 6.25em;
    }

    .make_timer_big {
        transition: all 0.50s;
        font-size: 13em;
        height: 220px;
        width: 400px;
    }

    .make_shrink_side_panel {
        transition: width 0.50s;
        width: 0%;
    }

    .make_grow_side_panel_content {
        transition: width 0.50s;
        transition-delay: 1s;
        overflow: hidden;
        width: 75%;
    }

    .make_shrink_side_panel_content {
        transition: width 0.50s;
        width: 0%;
    }

    .make_instant_open_side_panel_content {
        transition: width 1ms;
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

    .slide-up-enter-active,
    .slide-up-leave-active {
        transition: all 0.25s ease-out;
    }

    .slide-up-enter-from {
        opacity: 0;
        transform: rotateX(90deg);
        transform: rotateX(-90deg) translateY(-1em);

    }

    .slide-up-leave-to {
        opacity: 0;
        transform: rotateX(-90deg) translateY(1em);
    }
</style>
