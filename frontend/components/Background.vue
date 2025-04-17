<script setup lang="ts">
    import { ref } from 'vue';
    import OBSWebSocket from 'obs-websocket-js';
    import ScrollingTitle from './ScrollingTitle.vue';

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
        
    });

    obs.on("ConnectionError", () => {
        isObsConnected = false;
    });

    obs.on("ConnectionClosed", () => {
        isObsConnected = false;
    });

    if (isObsConnected) {
        const currObsSceneInfo = await obs.call("GetCurrentProgramScene");
        // updateValuesUsingSceneName(currObsSceneInfo.sceneName);
    }
</script>

<template>
    <div id="background">
        <ScrollingTitle text="SHADER" animDuration="5s" class="title-scroller title-scroller-shader" />
        <ScrollingTitle text="SHOWDOWN" animDuration="5s" reversed class="title-scroller title-scroller-showdown "/>
        <ScrollingTitle text="SHADER" animDuration="5s" class="title-scroller title-scroller-shader" />
        <ScrollingTitle text="SHOWDOWN" animDuration="5s" reversed class="title-scroller title-scroller-showdown "/>
        <ScrollingTitle text="SHADER" animDuration="5s" class="title-scroller title-scroller-shader" />
        <ScrollingTitle text="SHOWDOWN" animDuration="5s" reversed class="title-scroller title-scroller-showdown "/>
        <ScrollingTitle text="SHADER" animDuration="5s" class="title-scroller title-scroller-shader" />
        <ScrollingTitle text="SHOWDOWN" animDuration="5s" reversed class="title-scroller title-scroller-showdown "/>
    </div>
</template>

<style scoped>
    #background {
        transform: rotate(-10deg) scale(1.2);
    }

    .title-scroller {
        display: block;

        width: 100%;
        height: 200px;

        font-family: "Chivo", sans-serif;
        font-size: 12em;
        font-weight: 800;
        font-style: italic;
    }

    .title-scroller-shader {
        background-color: black;
        color: white;
    }

    .title-scroller-showdown {
        background-color: white;
        color: black;
    }
</style>
