<script setup lang="ts">
    import { ref } from 'vue';
    
    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);
    
    const line1Text = ref("SHADER");
    const line2Text = ref("SHOWDOWN");

    const line1TextArg = urlParams.get("line1text");
    const line2TextArg = urlParams.get("line2text");

    if (line1TextArg != null) line1Text.value = line1TextArg;
    if (line2TextArg != null) line2Text.value = line2TextArg;
</script>

<template>
    <div id="title">
        <div id="title-line1">
            <span id="title-line1-text">{{ line1Text }}</span>
            <span id="title-line1-text">{{ line1Text }}</span>
        </div>
        <div id="title-line2">
            <span id="title-line2-text">{{ line2Text }}</span>
            <span id="title-line2-text">{{ line2Text }}</span>
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
</style>
