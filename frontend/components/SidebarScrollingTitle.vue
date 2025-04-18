<script setup lang="ts">
    import { ref, defineProps, onMounted, onUpdated } from 'vue';

    const props = defineProps({
        text: {
            type: String,
            required: true
        },
        side: {
            type: String
        }
    });

    const sidebar_wrap = ref();
    const sidebar_before = ref();
    const sidebar_real = ref();
    const sidebar_after = ref();
    const side = ref(props.side?.toLowerCase() == "right" ? "right" : "left");
    
    function make() {
        var i = 0;
        var totalSize = 0;
        var realElementId = 2;
        
        const wrapHtmlElement = sidebar_wrap.value;
        const beforeHtmlElement = sidebar_before.value;
        const realHtmlElement = sidebar_real.value;
        const afterHtmlElement = sidebar_after.value;
        
        // Clearing bar content of previous letter nodes
        while (beforeHtmlElement.firstChild) {
            beforeHtmlElement.removeChild(beforeHtmlElement.firstChild);
        }

        while (realHtmlElement.firstChild) {
            realHtmlElement.removeChild(realHtmlElement.firstChild);
        }

        while (afterHtmlElement.firstChild) {
            afterHtmlElement.removeChild(afterHtmlElement.firstChild);
        }

        while (totalSize < (window.innerWidth / 2.)) {  // todo: prendre plutôt la width de l'element parent (si elle est bien set)
            for (let j = 0; j < props.text.length; j++) {
                var newSpan = document.createElement("span");

                newSpan.textContent = props.text[j];

                if (newSpan.textContent == " ") {
                    newSpan.textContent = ""
                    newSpan.innerHTML = "&nbsp";
                }

                if (i != realElementId) {
                    newSpan.classList.add("stroke-behind");
                    newSpan.classList.add("letter-do-fade-in-out");
                }
                else {
                    newSpan.classList.add("real-text");
                    newSpan.classList.add("stroke-behind");
                    newSpan.classList.add("letter-do-fade-in");
                }

                newSpan.style.opacity = "0";

                let animationDelay = 0.;
                
                // OBSOLETE. SEE CODE BELOW 
                // if (side.value == "left") {
                //     animationDelay = ((props.text.length*10) - (i * props.text.length + j)) * 0.01;
                // }
                // newSpan.style.animationDelay = animationDelay.toString() + "s";

                if (i < realElementId) beforeHtmlElement?.appendChild(newSpan);
                if (i == realElementId) realHtmlElement?.appendChild(newSpan);
                if (i > realElementId) {
                    afterHtmlElement?.appendChild(newSpan);
                    totalSize += newSpan.offsetWidth;
                }
            }

            i += 1;
        }

        if (side.value == "right") {
            let j = 0;

            for (let i = 0; i < afterHtmlElement.children.length; i++) {
                afterHtmlElement.children[i].style.animationDelay = (j * 0.01).toString() + 's';
                j++;
            }

            for (let i = 0; i < realHtmlElement.children.length; i++) {
                realHtmlElement.children[i].style.animationDelay = (j * 0.01).toString() + 's';
                j++;
            }

            for (let i = 0; i < beforeHtmlElement.children.length; i++) {
                beforeHtmlElement.children[i].style.animationDelay = (j * 0.01).toString() + 's';
                j++;
            }
        }
        else {
            let j = 0;

            for (let i = 0; i < beforeHtmlElement.children.length; i++) {
                beforeHtmlElement.children[i].style.animationDelay = ((afterHtmlElement.children.length - j - 1) * 0.01).toString() + 's';
                j++;
            }

            for (let i = 0; i < realHtmlElement.children.length; i++) {
                realHtmlElement.children[i].style.animationDelay = ((afterHtmlElement.children.length - j - 1) * 0.01).toString() + 's';
                j++;
            }

            for (let i = 0; i < afterHtmlElement.children.length; i++) {
                afterHtmlElement.children[i].style.animationDelay = ((afterHtmlElement.children.length - j - 1) * 0.01).toString() + 's';
                j++;
            }
        }
    }

    onMounted(() => {
        make();
    });

    onUpdated(() => {
        make();
    });
</script>

<template>
    <div>
        <div ref="sidebar_wrap" :class="side+'-sidebar-wrap '+side+'-sidebar-is-arriving'">
            <div ref="sidebar_before" :class="side+'-sidebar-before'"></div>
            <div ref="sidebar_real" :class="side+'-sidebar-real'"></div>
            <div ref="sidebar_after" :class="side+'-sidebar-after'"></div>
        </div>
    </div>
    <div class="side-panel-shutter" id="side-left-shutter"></div>
</template>

<style>
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
        display: inline;
        position: absolute;
        left: 0px;
    }

    .right-sidebar-wrap {
        display: inline;
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

    .stroke-behind {
        color: black;
        -webkit-text-stroke: 2px white;
        paint-order: stroke fill;
    }

    /* THROW THE REST?? | */
    /*                  V */
    .side-panel-shutter {
        position: absolute;
        height: 100%;
        background-color: black;
        top: 0;
        /* animation: 1s ease-in-out 0s shutter-animation infinite; */
    }

    #side-right-shutter {
        animation-direction: reverse;
    }

    @keyframes shutter-animation {
        0% {
            left: 0%;
            right: 100%;
        }
        50% {
            left: 0%;
            right: 0%;
        }
        100% {
            left: 100%;
            right: 0%;
        }
    }
</style>