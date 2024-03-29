<script setup lang="ts">
    import { ref } from 'vue';
    import OBSWebSocket from 'obs-websocket-js';
    
    // CONSTANTS
    const OBS_WS_ADDRESS = "ws://localhost:4455";
    const SERVER_WS_ADDRESS = "ws://localhost:6969";
    const SERVER_API_ADDRESS = "http://localhost:8080";
    const OBS_WS_PASSWORD = "meubapelefoute";

    // PROPS
    const line1Text = ref("PIPS");
    const line2Text = ref("POPS");
    const stageNum = ref(0);
    const currObsSceneName = ref("INTRO");

    // FLAGS
    var isObsConnected = false;


    function updateValuesUsingSceneName(sceneName: string) {
        currObsSceneName.value = sceneName;
    }


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

    if (isObsConnected) {
        const currObsSceneInfo = await obs.call("GetCurrentProgramScene");
        updateValuesUsingSceneName(currObsSceneInfo.sceneName);
    }
</script>

<template>
    <div id="title" class="slight-tilting">
        <div id="title-line1" class="slight-moving">
            <Transition name="slide-down-up">
                <span id="title-line1-stage2" v-if="currObsSceneName === 'INTRO_ROUND'">{{ line1Text }}</span>
                <span id="title-line1-stage3" v-else-if="currObsSceneName === 'INTRO_VS'">COOL TEXT</span>
                <span id="title-line1-stage1" v-else>SHADER</span>
            </Transition>
        </div>
        <div id="title-line2" class="slight-moving-reverse">
            <Transition name="slide-up-down">
                <span id="title-line2-stage2" v-if="currObsSceneName === 'INTRO_ROUND'">{{ line2Text }}</span>
                <span id="title-line2-stage3" v-else-if="currObsSceneName === 'INTRO_VS'">TEST2</span>
                <span id="title-line2-stage1" v-else>SHOWDOWN</span>
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

    #title-line1 span {
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

    #title-line2 span {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        line-height: 1em;
    }

    #title-line1-stage1 {
        font-size: 1em;
    }

    #title-line1-stage2 {
        font-size: 1em;
    }

    #title-line1-stage3 {
        font-size: 1em;
    }

    #title-line2-stage1 {
        font-size: 1em;
    }

    #title-line2-stage2 {
        font-size: 1em;
    }

    #title-line2-stage3 {
        font-size: 1em;
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
        margin-bottom: -400px;
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
        margin-top: -400px;
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
