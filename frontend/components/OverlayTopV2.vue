<script setup lang="ts">
    import { ref } from 'vue';
    import OBSWebSocket from 'obs-websocket-js';
    import ScrollingTitle from './ScrollingTitle.vue';

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
        if (sidePanelsVisibility.value) {
            var parentHtmlElement = document.getElementById("left-sidebar");
            if (parentHtmlElement) {
                makeSideBarHeader(parentHtmlElement, "ROUND");
            }
        }
    }

    function toggleTimerSize() {
        timerIsBig.value = !timerIsBig.value;
    }

    function makeSideBarHeader(parentHtmlElement: HTMLElement, text: string) {
        var i = 0;
        var totalSize = 0;
        var realElementId = 2;
        
        // Clearing bar content of previous letter nodes
        while (parentHtmlElement.firstChild) {
            parentHtmlElement.removeChild(parentHtmlElement.firstChild);
        }

        var wrapHtmlElement = document.createElement("div");

        var beforeHtmlElement = document.createElement("div");
        var realHtmlElement = document.createElement("div");
        var afterHtmlElement = document.createElement("div");
        
        wrapHtmlElement.classList.add("left-sidebar-wrap");
        wrapHtmlElement.classList.add("left-sidebar-is-arriving");

        beforeHtmlElement.className = "left-sidebar-before";
        realHtmlElement.className = "left-sidebar-real";
        afterHtmlElement.className = "left-sidebar-after";

        wrapHtmlElement?.appendChild(beforeHtmlElement);
        wrapHtmlElement?.appendChild(realHtmlElement);
        wrapHtmlElement?.appendChild(afterHtmlElement);

        parentHtmlElement?.appendChild(wrapHtmlElement);

        while (totalSize < (window.innerWidth / 2.)) {
            for (let j = 0; j < text.length; j++) {
                var newSpan = document.createElement("span");
                newSpan.textContent = text[j];

                if (newSpan.textContent == " ") {
                    newSpan.textContent = ""
                    newSpan.innerHTML = "&nbsp";

                }

                if (i != realElementId) {
                    newSpan.classList.add("stroke-behind");
                    newSpan.classList.add("letter-do-fade-in-out");
                }
                else {
                    newSpan.classList.add("real-text");
                    newSpan.classList.add("stroke-behind");
                    newSpan.classList.add("letter-do-fade-in");
                }


                newSpan.style.opacity = "0";
                newSpan.style.animationDelay = (((text.length*10) - (i * text.length + j)) * 0.01).toString() + "s";

                if (i < realElementId) beforeHtmlElement?.appendChild(newSpan);
                if (i == realElementId) realHtmlElement?.appendChild(newSpan);
                if (i > realElementId) {
                    afterHtmlElement?.appendChild(newSpan);
                    totalSize += newSpan.offsetWidth;
                }
            }

            i += 1;
        }

        //newSpan.className = "stroke-behind";
            
        //newSpan.style.position = "absolute";
        //newSpan.style.left = (i * 1).toString() + "em";
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
            timer.value = Math.floor(Math.max(newTimerValue, 0));
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

        <div id="left-sidebar" style="margin: 20px; margin-top: 10px;"></div>

        <!---
        <div class="side-panel-content" id="side-left-content" :class="{
            make_grow_side_panel_content: sidePanelsVisibility,
            make_shrink_side_panel_content: !sidePanelsVisibility }">

            <div style="margin: 20px; margin-top: 10px; color: black;">{{ roundName.toUpperCase() }}</div>
        </div>
        -->
        
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

            <div id="timer-text" :class="{ blink: isTimerBlinking }">
                <!--{{ Math.floor(timer / 60).toString().padStart(2, '0') }}:{{ Math.floor(timer % 60).toString().padStart(2, '0') }}-->
                <div class="timer-digit-wrap">
                    <div class="timer-digit-container">
                        <Transition name="slide-up">
                            <span class="timer-digit">
                                {{ Math.floor(timer / 60).toString().padStart(2, '0')[0] }}
                            </span>
                        </Transition>
                    </div>
                </div>
                <div class="timer-digit-wrap">
                    <div class="timer-digit-container">
                        <Transition name="slide-up">
                            <span class="timer-digit">
                                {{ Math.floor(timer / 60).toString().padStart(2, '0')[1] }}
                            </span>
                        </Transition>
                    </div>
                </div>
                <div class="timer-digit-wrap">
                    <div class="timer-digit-container" style="width: 0.40ch">
                        <span class="timer-digit" style="width: auto">:</span>
                    </div>
                </div>
                <div class="timer-digit-wrap">
                    <div class="timer-digit-container">
                        <Transition name="slide-up">
                            <span class="timer-digit">
                                {{ Math.floor(timer % 60).toString().padStart(2, '0')[0] }}
                            </span>
                        </Transition>
                    </div>
                </div>
                <div class="timer-digit-wrap">
                    <div class="timer-digit-container">
                        <Transition name="slide-up">
                            <span class="timer-digit" :key="timer">
                                {{ Math.floor(timer % 60).toString().padStart(2, '0')[1] }}
                            </span>
                        </Transition>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <ScrollingTitle text="SHADER" class="title-scroller title-scroller-shader" />
    <ScrollingTitle text="SHOWDOWN" reversed class="title-scroller title-scroller-showdown "/>

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
    <button type="button" @click="startTestAnim" style="position: absolute; bottom: 0px; left: 80%;">
        TestAnim
    </button>
</template>

<!--- scoped --->
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

    .left-sidebar-before {
        display: block;
        position: absolute;
        right: 100%;
        top: 0;
    }


    .left-sidebar-real {
        
    }

    .left-sidebar-after {
        display: block;
        position: absolute;
        left: 100%;
        top: 0;
    }

    .left-sidebar-wrap {
        display: inline;
        position: absolute;
        /* left: 20px; */
    }

    .left-sidebar-wrap span {

    }

    @keyframes left-sidebar-arrive {
        0% {
            left: 400px
        }
        100% {
            left: 20px
        }
    }

    .left-sidebar-is-arriving {
        animation: left-sidebar-arrive 1s ease-out 0s 1;
    }

    .stroke-behind {
        color: black;
        -webkit-text-stroke: 2px white;
        paint-order: stroke fill;
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

    @keyframes letter-fade-in {
        0% {
            opacity: 0%;
            color: black;
        }
        50% {
            -webkit-text-stroke-color: white;
            opacity: 100%;
            color: black;
        }
        100% {
            -webkit-text-stroke-color: black;
            opacity: 100%;
            color: white;
        }
    }

    @keyframes letter-fade-in-out {
        0% {
            opacity: 0%;
        }
        50% {
            opacity: 100%;
        }
        100% {
            opacity: 0%;
        }
    }

    .letter-do-fade-in-out {
        animation: 0.75s linear 1s 1 letter-fade-in-out; /* 0.5s */
    }

    .letter-do-fade-in {
        animation: 0.75s linear 1s 1 letter-fade-in ; /* 0.5s */
        animation-fill-mode: forwards;
        animation-direction: normal;
    }


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

    .slide-up-enter-active,
    .slide-up-leave-active {
        transition: all 0.25s ease-out;
    }

    .slide-up-enter-from {
        opacity: 0;
        transform: translateY(1em);
    }

    .slide-up-leave-to {
        opacity: 0;
        transform: translateY(-1em);
    }

    .title-scroller {
        display: block;
        width: 100%;
        height: 200px;
        position: absolute;
        background-color: black;
        font-size: 9em;
        font-family: "Chivo", sans-serif;
        font-size: 12em;
    }

    .title-scroller-shader {
        top: 300px;
    }

    .title-scroller-showdown {
        top: 500px;
    }

</style>

