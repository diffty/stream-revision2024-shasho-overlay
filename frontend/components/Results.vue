<script setup lang="ts">
    import { ref } from 'vue';
    import OBSWebSocket from 'obs-websocket-js';
    
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

    const coderRank1Name = ref("");
    const coderRank2Name = ref("");
    const coderRank3Name = ref("");
    const coderRank1Votes = ref(0);
    const coderRank2Votes = ref(0);
    const coderRank3Votes = ref(0);

    var config: Config;


    async function updateResults() {
        const results = await fetch(`${SERVER_API_ADDRESS}/round_results`)
            .catch((e: Error) => {
                console.error(`Can't retrieve current round infos : ${e}`)
            });

        console.log(results);
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
        console.log(eventMsg);

        switch (eventMsg.type) {
            case "UpdateResultsEvent":
                coderRank1Name.value = eventMsg.payload.coderRank1Name;
                coderRank2Name.value = eventMsg.payload.coderRank2Name;
                coderRank3Name.value = eventMsg.payload.coderRank3Name;
                coderRank1Votes.value = eventMsg.payload.coderRank1Votes;
                coderRank2Votes.value = eventMsg.payload.coderRank2Votes;
                coderRank3Votes.value = eventMsg.payload.coderRank3Votes;
                break;
        }
    })
</script>

<template>
    <div id="coderRank1" class="coderLine">
        <span class="coderRank">#1</span><span class="coderName">{{ coderRank1Name }}</span> <span class="coderVotes">({{ coderRank1Votes }})</span>
    </div>

    <div id="coderRank2" class="coderLine">
        <span class="coderRank">#2 </span><span class="coderName">{{ coderRank2Name }}</span> <span class="coderVotes">({{ coderRank2Votes }})</span>
    </div>

    <div id="coderRank3" class="coderLine">
        <span class="coderRank">#3 </span><span class="coderName">{{ coderRank3Name }}</span> <span class="coderVotes">({{ coderRank3Votes }})</span>
    </div>
</template>

<style scoped>
    @font-face {
        font-family: "Tungsten-Bold-TD";
        src: url("./assets/fonts/Tungsten-Bold-TD.woff") format("woff");
        font-weight: normal;
        font-style: normal;
    }

    * {
        font-family: "Chivo", sans-serif;
        /* color: white; */
    }

    .coderLine {
        margin-top: 20px;
        margin-bottom: 20px;
    }

    #coderRank1 > .coderName {
        font-size: 200px;
    }

    #coderRank2 > .coderName {
        font-size: 150px;
    }

    #coderRank3 > .coderName {
        font-size: 110px;
    }

    #coderRank1 > .coderRank {
        font-size: 200px;
    }

    #coderRank2 > .coderRank {
        font-size: 150px;
    }

    #coderRank3 > .coderRank {
        font-size: 110px;
    }

    .coderName {
        font-weight: bold;
        margin-left: 30px;
        margin-right: 30px;
    }

    .coderRank {
        font-weight: bold;
    }

    .coderVotes {
        font-style: italic;
        font-size: 80px;
    }
</style>
