<!-- TODO:
barre qui se déplir avec le pseudo sous le timer
animation de réduction du timer
apparition des textres gauche et droite

bannière full white ?? (même les deux côtés ?)
-->

<script setup lang="ts">
    import { ref } from 'vue';
    import OBSWebSocket from 'obs-websocket-js';

    // defineProps<{ nick: string }>()

    type Config = {
        currRoundId: number;
        rounds: Array<Array<string>>;
        roundName: string;
        djName: string;
        commentatorName: string;
        hostName: string;
    };

    const infoStripText = ref("")
    const sidePanelsVisibility = ref(true)
    const timerIsBig = ref(true)
    const isBottomInfoStripVisible = ref(false)
    const isBottomInfoStripTransitionActive = ref(false)
    const coderName1 = ref("");
    const coderName2 = ref("");
    const coderName3 = ref("");
    const currCoderName = ref("");
    const roundName = ref("");
    const djName = ref("");
    const commentatorName = ref("");
    const hostName = ref("");

    var config: Config;

    const configFile = await fetch("./config.json")
    if (configFile.status == 200) {
        console.log("Config loaded!")
        config = await configFile.json();

        const currRoundId = config.currRoundId;
        coderName1.value = config.rounds[currRoundId][0];
        coderName2.value = config.rounds[currRoundId][1];
        coderName3.value = config.rounds[currRoundId][2];
        roundName.value = config.roundName;
        djName.value = config.djName;
        commentatorName.value = config.commentatorName;
        hostName.value = config.hostName;
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
                currCoderName.value = config.rounds[config.currRoundId][coderId];
                infoStripText.value = config.rounds[config.currRoundId][coderId];
            }
        }
    }
    const obs = new OBSWebSocket();

    await obs.connect("ws://192.168.1.47:4455", "vWbRjK35sRMOZPAy");

    obs.on("SceneTransitionStarted", async function (evt: object) {
        const nextSceneInfo = await obs.call("GetCurrentProgramScene");
        updateValuesUsingSceneName(nextSceneInfo.currentProgramSceneName);
    });

    const currObsSceneInfo = await obs.call("GetCurrentProgramScene");
    updateValuesUsingSceneName(currObsSceneInfo.sceneName);

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
    </div>

    <div id="container">
        <div id="bar-center" :class="{
            make_timer_small: !timerIsBig,
            make_timer_big: timerIsBig }">

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
                    <div id="bar-bottom-info-text" :key="bar_bottom_info_text_content">
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

            <div id="timer-text">00:00</div>
        </div>
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

    #container {
        display: flex;
        /*overflow: hidden;*/
        white-space: nowrap;
        align-items: center;
        justify-content: center;
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
        height: 40px;
        /* margin-bottom: -0.35em; */
        bottom: 0em;
        z-index: -10;
    }

    #bar-bottom-info-text {
        color: white;
        font-size: 36px;
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

    #timer-text {
        position: absolute;
        width: 100%;
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
        width: 250px;
        font-size: 6em;
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
        margin-bottom: -40px;
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

