<script setup lang="ts">
    import { ref } from 'vue';
    import OBSWebSocket from 'obs-websocket-js';
    
    // CONSTANTS
    const OBS_WS_ADDRESS = "ws://localhost:4455";
    const SERVER_WS_ADDRESS = "ws://localhost:6969";
    const SERVER_API_ADDRESS = "http://localhost:8080";
    const OBS_WS_PASSWORD = "meubapelefoute";

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

    var config: Config;

    function updateValuesUsingSceneName(sceneName: string) {
        currObsSceneName.value = sceneName;
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
</script>

<template>
    <div id="title" class="slight-tilting">
        <div id="title-line1" class="slight-moving">
            <Transition name="slide-down-up">
                <span id="title-line1-stage2" class="title-stage-line" v-if="currObsSceneName === 'INTRO_ROUND'">{{ roundName }}</span>
                <span id="title-line1-stage3" class="title-stage-line" v-else-if="currObsSceneName === 'INTRO_VS'">{{ roundName }}</span>
                <span id="title-line1-stage1" class="title-stage-line" v-else>SHADER</span>
            </Transition>
        </div>
        <div id="title-line2" class="slight-moving-reverse">
            <Transition name="slide-up-down">
                <span id="title-line2-stage2" class="title-stage-line" v-if="currObsSceneName === 'INTRO_ROUND'">
                    <div style="line-height: 0.8em; margin-top: 0.1em">COMMENTARY <br />{{ commentsName }}</div>
                    <div style="line-height: 0.8em; margin-top: 0.3em">DJ SET <br />{{ djName }}</div>
                </span>
                <span id="title-line2-stage3" class="title-stage-line" v-else-if="currObsSceneName === 'INTRO_VS'">
                    {{ coderName1 }}<br />
                    <span class="small-versus">VS</span> {{ coderName2 }}<br />
                    <span class="small-versus">VS</span> {{ coderName3 }}</span>
                <span id="title-line2-stage1" class="title-stage-line" v-else>SHOWDOWN</span>
            </Transition>
        </div>
    </div>
</template>

<style scoped>
    @font-face {
        font-family: "Tungsten-Bold-TD";
        src: url("./assets/fonts/Tungsten-Bold-TD.woff") format("woff");
    }

    #title {
        font-family: "Chivo", sans-serif;
        font-optical-sizing: auto;
        font-weight: 800;
        font-style: italic;
        text-align: center;
        transform: rotate(-5deg);
        filter: blur(0.01px);
        position: absolute;
        top: -10%;
        left: -10%;
        width: 120%;
        height: 120%;
    }

    #title-line1 {
        position: absolute;
        top: 0;
        bottom: 50%;
        left: 0;
        right: 0;
        background-color: white;
        font-size: 23.5em;
        color: black;
        vertical-align: bottom;
        overflow: hidden;
    }

    #title-line1 .title-stage-line {
        position: absolute;
        bottom: 0;
        left: 0;
        width: 100%;
        line-height: 1em;
    }

    #title-line2 {
        position: absolute;
        top: 50%;
        left: 0;
        background-color: black;
        font-size: 15em;
        color: white;
        height: 50%;
        width: 100%;
        line-height: 1em;
        overflow: hidden;
    }

    #title-line2 .title-stage-line {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        line-height: 0.8em;
    }

    #title-line1-stage1 {
        font-size: 1em;
    }

    #title-line1-stage2 {
        font-size: 0.55em;
    }

    #title-line1-stage3 {
        font-size: 0.55em;
    }

    #title-line2-stage1 {
        font-size: 1em;
        padding-top: 0.15em;
    }

    #title-line2-stage2 {
        font-size: 0.55em;
        padding-top: 0.15em;
    }

    #title-line2-stage3 {
        font-size: 0.7em;
        padding-top: 0.15em;
    }

    .small-versus {
        position: relative;
        font-size: 0.5em;
        line-height: 0;
        vertical-align: middle;
    }

    /* Transitions */
    .slide-down-up-enter-active {
        transition: margin-bottom 0.5s ease;
        transition-delay: 0.25s;
    }
    .slide-down-up-leave-active {
        transition: margin-bottom 0.5s ease;
    }

    .slide-down-up-enter-from,
    .slide-down-up-leave-to {
        margin-bottom: -650px;
    }

    .slide-up-down-enter-active {
        transition: margin-top 0.5s ease;
        transition-delay: 0.25s;
    }
    .slide-up-down-leave-active {
        transition: margin-top 0.5s ease;
    }

    .slide-up-down-enter-from,
    .slide-up-down-leave-to {
        margin-top: -650px;
    }

    /* Animations */
    @keyframes slight-tilt {
        0% {
            transform: rotate(4deg);
        }
        50% {
            transform: rotate(-4deg);
        }
        100% {
            transform: rotate(4deg);
        }
    }

    .slight-tilting {
        animation: slight-tilt 20s ease-in-out infinite;
    }

    @keyframes slight-move {
        from {
            margin-left: -50px;
        }
        to {
            margin-left: 50px;
        }
    }

    .slight-moving {
        animation: slight-move 10s ease-in-out infinite alternate-reverse;
    }

    .slight-moving-reverse {
        animation: slight-move 10s ease-in-out infinite alternate;
    }
</style>
