<script setup lang="ts">
    import { ref } from 'vue'

    defineProps<{ nick: string }>()

    const shrinked = ref(false)

    function toggleShrink() {
        shrinked.value = !shrinked.value
    }
</script>

<template>
    <div class="side-text" id="side-left-text">
        QUARTERS
    </div>
    
    <div class="side-text" id="side-right-text">
        ALKAMA
    </div>

    <div id="parent">
        <div id="container">
            <div id="bar-left-edge">
                <svg viewBox="0 0 100 100" preserveAspectRatio="none" style="width: 100%; height: 100%;">
                    <polygon points="0,0 100,0 100,100" style="fill: white;"></polygon>
                </svg>
            </div>
            
            <div id="bar-center" :class="{ make_grow_topbar: !shrinked, make_shrink_topbar: shrinked }">
                <span>00:00</span>
            </div>

            <div id="bar-right-edge">
                <svg viewBox="0 0 100 100" preserveAspectRatio="none" style="width: 100%; height: 100%;">
                    <polygon points="0,0 100,0 0,100" style="fill: white;"></polygon>
                </svg>
            </div>
        </div>
    </div>

    <button type="button" @click="toggleShrink" style="position: absolute">Toggle shape: {{ shrinked }}</button>

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

    .side-text {
        background-color: black;
        color: white;
        font-family: 'Tungsten-Bold-TD';
        font-size: 5em;
        line-height: 100%;
    }

    #side-left-text {
        position: fixed;
        left: 0;
        right: 50%;
        top: 0;
        height: 100px;
    }

    #side-right-text {
        position: fixed;
        left: 50%;
        right: 0;
        top: 0;
        height: 100px;
        text-align: right;
    }

    #container {
        display: flex;
        overflow: hidden;
        white-space: nowrap;
        align-items: center;
        justify-content: center;
        height: 150px;
    }

    #bar-left-edge {
        flex: 0 0 auto;
        width: 30px;
        height: 100%;
    }

    #bar-center {
        font-family: 'Tungsten-Bold-TD';
        font-size: 9em;
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
        width: 30px;
        height: 100%;
    }

    .make_grow_topbar {
        transition: width 0.50s;
        width: 100%;
    }

    .make_shrink_topbar {
        transition: width 0.50s;
        width: 350px;
    }
</style>
