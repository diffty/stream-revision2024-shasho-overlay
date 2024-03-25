<!-- TODO:
barre qui se déplir avec le pseudo sous le timer
animation de réduction du timer
apparition des textres gauche et droite

bannière full white ?? (même les deux côtés ?)
-->

<script setup lang="ts">
    import { ref } from 'vue'

    defineProps<{ nick: string }>()

    const timerWidthShrinked = ref(true)
    function toggleTimerWidthShrinked() {
        timerWidthShrinked.value = !timerWidthShrinked.value
    }

    const sidePanelsVisibility = ref(true)
    function toggleSidePanelsVisibility() {
        sidePanelsVisibility.value = !sidePanelsVisibility.value
    }

    const timerIsBig = ref(true)
    function toggleTimerSize() {
        timerIsBig.value = !timerIsBig.value
    }
</script>

<template>
    <div class="side-panel" id="side-left-title" :class="{ make_grow_side_panel: !sidePanelsVisibility, make_shrink_side_panel: sidePanelsVisibility }">
        <div style="margin: 20px; margin-top: 10px;">ROUND</div>

        <div class="side-panel-content" id="side-left-content" :class="{ make_grow_side_panel_content: !sidePanelsVisibility, make_shrink_side_panel_content: sidePanelsVisibility }">
            <div style="margin: 20px; margin-top: 10px; color: black;">QUARTERS</div>
        </div>
    </div>
    
    <div class="side-panel" id="side-right-title" :class="{ make_grow_side_panel: !sidePanelsVisibility, make_shrink_side_panel: sidePanelsVisibility }">
        <div style="margin: 20px; margin-top: 10px;">MUSIC</div>

        <div class="side-panel-content" id="side-right-content" :class="{ make_grow_side_panel_content: !sidePanelsVisibility, make_shrink_side_panel_content: sidePanelsVisibility }">
            <div style="margin: 20px; margin-top: 10px; color: black;">ALKAMA</div>
        </div>
    </div>

    <div id="parent">
        <div id="container">
            <div id="bar-left-edge">
                <svg viewBox="0 0 100 100" preserveAspectRatio="none" style="width: 100%; height: 100%;">
                    <polygon points="0,0 100,0 100,100" style="fill: white;"></polygon>
                </svg>
            </div>
            
            <div id="bar-center" :class="{
                    make_grow_topbar: !timerWidthShrinked,
                    make_shrink_topbar: timerWidthShrinked,
                    make_timer_small: !timerIsBig,
                    make_timer_big: timerIsBig,
                }">

                <span>00:00</span>
            </div>

            <div id="bar-right-edge">
                <svg viewBox="0 0 100 100" preserveAspectRatio="none" style="width: 100%; height: 100%;">
                    <polygon points="0,0 100,0 0,100" style="fill: white;"></polygon>
                </svg>
            </div>
        </div>
    </div>

    <button type="button" @click="toggleTimerWidthShrinked" style="position: absolute; bottom: 0px; left: 0%;">
        Toggle timer: {{ timerWidthShrinked }}
    </button>
    <button type="button" @click="toggleSidePanelsVisibility" style="position: absolute; bottom: 0px; left: 20%;">
        Toggle edge: {{ sidePanelsVisibility }}
    </button>
    <button type="button" @click="toggleTimerSize" style="position: absolute; bottom: 0px; left: 40%;">
        Toggle timer: {{ timerIsBig }}
    </button>
</template>

<style scoped>
    @font-face {
        font-family: "Tungsten-Bold-TD";
        src: url("../assets/fonts/Tungsten-Bold-TD.woff") format("woff");
    }

    #parent {
        position: fixed;
        left: -100px;
        right: -100px;
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
        overflow: hidden;
        white-space: nowrap;
        align-items: center;
        justify-content: center;
        height: 250px;
    }

    #bar-left-edge {
        flex: 0 0 auto;
        width: 50px;
        height: 100%;
    }

    #bar-center {
        font-family: 'Tungsten-Bold-TD';
        line-height: 100%;
        height: 100%;
        background-color: white;
        /*-webkit-text-stroke: 1px;
        -webkit-text-stroke-color: black;*/
        color: black;
        text-align: center;
    }

    #bar-right-edge {
        flex: 0 0 auto;
        width: 50px;
        height: 100%;
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
        font-size: 8em;
        width: 15%;
        height: 10%;
    }

    .make_timer_big {
        transition: all 0.50s;
        font-size: 15em;
        width: 25%;
        height: 100px;
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

    button {
        font-size: 30px;
        width: 300px;
        height: 100px;
    }
</style>
