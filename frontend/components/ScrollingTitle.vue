<script setup lang="ts">
    import { ref, onMounted } from 'vue';

    const title = ref();
    const title_content = ref();
    const scrolling_title_singletext_subwrap = ref();

    function makeScrollingTitleStrip(parentHtmlElement: HTMLElement, text: string) {
        var i = 0;
        var totalSize = 0;
        var realElementId = 1;
        
        var wrapHtmlElement = scrolling_title_singletext_subwrap.value;

        var beforeHtmlElement = document.createElement("div");
        var realHtmlElement = document.createElement("div");
        var afterHtmlElement = document.createElement("div");
        
        wrapHtmlElement.classList.add("is_scrolling_reverse");

        beforeHtmlElement.className = "scrolling-title-singletext-before";
        realHtmlElement.className = "scrolling-title-singletext-real";
        afterHtmlElement.className = "scrolling-title-singletext-after";

        wrapHtmlElement?.appendChild(beforeHtmlElement);
        wrapHtmlElement?.appendChild(realHtmlElement);
        wrapHtmlElement?.appendChild(afterHtmlElement);

        // parentHtmlElement?.appendChild(wrapHtmlElement);

        while (totalSize < (parentHtmlElement.offsetWidth)) {
            var newSpan = document.createElement("span");
            newSpan.innerHTML = text.replace(" ", "&nbsp;");

            if (i < realElementId) beforeHtmlElement?.appendChild(newSpan);
            if (i == realElementId) realHtmlElement?.appendChild(newSpan);
            if (i > realElementId) {
                afterHtmlElement?.appendChild(newSpan);
                totalSize += newSpan.offsetWidth;
            }

            i += 1;
        }
    }

    onMounted(() => {
        makeScrollingTitleStrip(title_content.value, "ZIZICACA PENIS")
    })
</script>

<template>
    <div ref="title" id="title_strip">
        <div ref="title_content" id="title_content">
            <div ref="scrolling_title_singletext_wrap" id="scrolling-title-singletext-wrap">
                <div ref="scrolling_title_singletext_subwrap" id="scrolling-title-singletext-subwrap">

                </div>
            </div>
        </div>
    </div>
</template>

<style>
    @keyframes scrolling {
        0% {
            left: 0%;
        }
        100% {
            left: 100%;
        }
    }

    .is_scrolling {
        animation: scrolling 1s linear 0s infinite; 
    }

    .is_scrolling_reverse {
        animation: scrolling 1s linear 0s infinite reverse; 
    }

    #title_strip {
        display: block;
        width: 100%;
        height: 150px;
        position: absolute;
        top: 300px;
        background-color: black;
        font-size: 9em;
        margin: 0;
        padding: 0;
        line-height: 100%;
        overflow: hidden;
    }

    #title_content {
        display: inline;
        position: absolute;
        width: 100%;

    }

    .scrolling-title-singletext-before {
        display: block;
        position: absolute;
        right: 100%;
        top: 0;
    }

    .scrolling-title-singletext-real {
        
    }

    .scrolling-title-singletext-after {
        display: block;
        position: absolute;
        left: 100%;
        top: 0;
    }

    #scrolling-title-singletext-wrap {
        display: inline;
        position: absolute;
    }


    #scrolling-title-singletext-subwrap {
        position: relative;
    }

</style>
