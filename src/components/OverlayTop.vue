<script setup lang="ts">
    import { ref } from 'vue'

    defineProps<{ nick: string }>()

    const shrinked = ref(false)

    function toggleShrink() {
        shrinked.value = !shrinked.value
    }
</script>

<template>
    <div id="side-left-text">
        TEST
    </div>
    
    <div id="side-right-text">
        TEST
    </div>
   

    <div id="parent">
        <div id="container">
            <div id="bar-left-edge">
                <svg viewBox="0 0 100 100" style="display: block; position: relative;">
                    <polygon points="0,0 100,0 100,100" style="fill: white;"></polygon>
                </svg>
            </div>
            
            <div id="bar-center" :class="{ make_grow_topbar: !shrinked, make_shrink_topbar: shrinked }">
                <span>00:00</span>
            </div>

            <div id="bar-right-edge">
                <svg viewBox="0 0 100 100" style="display: block; position: relative;">
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

    #side-left-text {
        position: fixed;
        left: 0;
        right: 50%;
        top: 0;
        height: 100px;
        background-color: red;
    }

    #side-right-text {
        position: fixed;
        left: 50%;
        right: 0;
        top: 0;
        height: 100px;
        background-color: red;
    }

    #parent {
        position: fixed;
        left: -100px;
        right: -100px;
    }

    #container {
        display: flex;
        overflow: hidden;
        white-space: nowrap;
        align-items: center;
        justify-content: center;
        height: 100px;
    }

    #bar-left-edge {
        flex: 0 0 auto;
        width: 100px;
        height: 100%;
    }

    #bar-center {
        font-family: 'Tungsten-Bold-TD';
        font-size: 5em;
        height: 100%;
        background-color: white;
        /*-webkit-text-stroke: 1px;
        -webkit-text-stroke-color: black;*/
        color: white;
        text-align: center;
    }

    #bar-right-edge {
        flex: 0 0 auto;
        width: 100px;
        height: 100%;
        /* background-color: blue; */
    }

    .make_grow_topbar {
        transition: width 0.80s;
        width: 100%;
    }

    .make_shrink_topbar {
        transition: width 0.80s;
        width: 400px;
    }
</style>
