<script setup lang="ts">
    import { ref, defineProps, onMounted, onUpdated } from 'vue';

    const props = defineProps({
        text: {
            type: String,
            required: true
        },
        side: {
            type: String
        },
        visible: {
            type: Boolean
        }
    });

    const sidebar_wrap = ref();
    const sidebar_real = ref();
    const sidebar_title_text = ref();
    const sidebar_parent = ref();
    const side = ref(props.side?.toLowerCase() == "right" ? "right" : "left");
    
    var wrapHtmlElement = sidebar_wrap.value;
    var realHtmlElement = sidebar_real.value;

    function clear() {
        // Clearing bar content of previous letter nodes
        while (realHtmlElement.firstChild) {
            realHtmlElement.removeChild(realHtmlElement.firstChild);
        }
    }

    function make() {
        var i = 0;
        var totalSize = 0;
        var realElementId = 1;
        
        // clear();

        // var newSpan = document.createElement("span");

        // newSpan.textContent = props.text;
        // newSpan.classList.add("real-text");

        // realHtmlElement?.appendChild(newSpan);

        // if (side.value == "right") {
        //     let j = 0;

        //     for (let i = 0; i < realHtmlElement.children.length; i++) {
        //         realHtmlElement.children[i].style.animationDelay = (j * 0.01).toString() + 's';
        //         j++;
        //     }
        // }
        // else {
        //     let j = 0;
        //     for (let i = 0; i < realHtmlElement.children.length; i++) {
        //         realHtmlElement.children[i].style.animationDelay = ((afterHtmlElement.children.length - j - 1) * 0.01).toString() + 's';
        //         j++;
        //     }
        // }

        // sidebar_wrap.value.classList.add(side.value + "-sidebar-is-arriving")

        // sidebar_wrap.value.addEventListener("animationend", (e: any) => {
        //     sidebar_wrap.value.classList.remove(side.value + "-sidebar-is-arriving")
        // });
    }

    onMounted(() => {

        // make();
    });

    onUpdated(() => {

        /*if (props.text == "") {
            clear();
        }
        else {
            make();
        }*/
    });
</script>

<template>
    <div ref="sidebar_parent">
        <div ref="sidebar_wrap" :class="side+'-sidebar-wrap'">
            <Transition :name="'slide-'+side">
                <div ref="sidebar_real" :class="side+'-sidebar-real'" :key="props.text">{{ props.text }}</div>
            </Transition>
        </div>
    </div>
    <div class="side-panel-shutter" id="side-left-shutter"></div>
</template>

<style scoped>
    .left-sidebar-before {
        display: block;
        position: absolute;
        right: 100%;
        top: 0;
    }

    .left-sidebar-after {
        display: block;
        position: absolute;
        left: 100%;
        top: 0;
    }

    .right-sidebar-before {
        display: block;
        position: absolute;
        left: 100%;
        top: 0;
    }

    .right-sidebar-after {
        display: block;
        position: absolute;
        right: 100%;
        top: 0;
    }

    .left-sidebar-wrap {
        display: block;
        position: absolute;
        left: 0px;
    }

    .right-sidebar-wrap {
        display: block;
        position: absolute;
        right: 0px;
    }

    @keyframes left-sidebar-arrive {
        0% {
            left: 400px
        }
        100% {
            left: 0px
        }
    }

    .left-sidebar-is-arriving {
        animation: left-sidebar-arrive 1s ease-out 0s 1;
    }

    @keyframes right-sidebar-arrive {
        0% {
            right: 400px
        }
        100% {
            right: 0px
        }
    }

    .right-sidebar-is-arriving {
        animation: right-sidebar-arrive 1s ease-out 0s 1;
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

    .letter-do-fade-out {
        animation: 0.75s linear 1s 1 letter-fade-in ; /* 0.5s */
        animation-fill-mode: backwards;
        animation-direction: reverse;
    }

    .stroke-behind {
        color: black;
        -webkit-text-stroke: 2px white;
        paint-order: stroke fill;
    }


    .slide-left-enter-active,
    .slide-left-leave-active {
        transition: all 0.5s ease;
    }

    .slide-left-enter-from {
        opacity: 0;
        margin-left: -100px;
    }
    .slide-left-enter-to,
    .slide-left-leave-from {
        opacity: 1;
        margin-left: 0px;
    }
    .slide-left-leave-to {
        opacity: 0;
        margin-left: 100px;
    }

    .slide-right-enter-active,
    .slide-right-leave-active {
        transition: all 0.5s ease;
    }

    .slide-right-enter-from {
        opacity: 0;
        margin-right: -100px;
    }
    .slide-right-enter-to,
    .slide-right-leave-from {
        opacity: 1;
        margin-right: 0px;
    }
    .slide-right-leave-to {
        opacity: 0;
        margin-right: 100px;
    }
</style>