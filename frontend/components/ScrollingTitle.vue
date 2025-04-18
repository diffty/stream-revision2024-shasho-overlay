<script setup lang="ts">
    import { ref, onMounted } from 'vue';

    const title = ref();
    const title_content = ref();
    const scrolling_title_singletext_subwrap = ref();
    const scrolling_title_singletext_before = ref();
    const scrolling_title_singletext_real = ref();
    const scrolling_title_singletext_after = ref();

    const props = defineProps({
        reversed: Boolean,
        text: {
            type: String,
            required: true
        },
        animDuration: {
            type: Number,
        }
    });

    const animDuration = ref(props.animDuration || "2s");
    
    onMounted(() => {
        var totalSize = 0;
        var realElementId = 1;
        
        var wrapHtmlElement = scrolling_title_singletext_subwrap.value;
        if (props.reversed)
            wrapHtmlElement.classList.add("is_scrolling_reverse");
        else
            wrapHtmlElement.classList.add("is_scrolling");

        var i = 0;
        while (totalSize < (title_content.value.offsetWidth)) {
            var newSpan = document.createElement("span");
            newSpan.innerHTML = props.text.replace(" ", "&nbsp;");

            if (i < realElementId) {
                scrolling_title_singletext_before.value.appendChild(newSpan);
            }
            else if (i == realElementId) {
                scrolling_title_singletext_real.value.appendChild(newSpan);
            }
            if (i > realElementId) {
                scrolling_title_singletext_after.value.appendChild(newSpan);
                totalSize += newSpan.offsetWidth;
            }

            i += 1;
        }
    })
</script>

<template>
    <div ref="title" id="title_strip">
        <div ref="title_content" id="title_content">
            <div ref="scrolling_title_singletext_wrap" id="scrolling-title-singletext-wrap">
                <div ref="scrolling_title_singletext_subwrap" id="scrolling-title-singletext-subwrap">
                    <div ref="scrolling_title_singletext_before" id="scrolling-title-singletext-before"></div>
                    <div ref="scrolling_title_singletext_real" id="scrolling-title-singletext-real"></div>
                    <div ref="scrolling_title_singletext_after" id="scrolling-title-singletext-after"></div>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
    @keyframes scrolling {
        0% {
            left: 0%;
        }
        100% {
            left: 100%;
        }
    }

    .is_scrolling {
        animation: scrolling v-bind('animDuration') linear 0s infinite; 
    }

    .is_scrolling_reverse {
        animation: scrolling v-bind('animDuration') linear 0s infinite reverse; 
    }

    #title_strip {
        margin: 0;
        padding: 0;
        line-height: 100%;
        overflow: hidden;
    }

    #title_content {
        /* display: inline; */
        position: absolute;
        width: 100%;
        white-space: nowrap;
    }

    #scrolling-title-singletext-before {
        display: block;
        position: absolute;
        right: 100%;
        top: 0;
    }

    #scrolling-title-singletext-real {
        
    }

    #scrolling-title-singletext-after {
        display: block;
        position: absolute;
        left: 100%;
        top: 0;
    }

    #scrolling-title-singletext-wrap {
        /* display: inline; */
        position: absolute;
    }


    #scrolling-title-singletext-subwrap {
        position: relative;
    }

    .stroke-behind {
        color: red;
        -webkit-text-stroke: 5px white;
        paint-order: stroke fill;
    } 
</style>
