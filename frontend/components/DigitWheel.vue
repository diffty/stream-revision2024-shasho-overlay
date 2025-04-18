<script setup lang="ts">
    import { ref, onMounted } from 'vue';

    const props = defineProps({
        num: String
    });

</script>

<template>
    <div class="timer-digit-wrap">
        <div class="timer-digit-container">
            <Transition name="slide-up">
                <span class="timer-digit" :key="props.num">
                    {{ props.num }}
                </span>
            </Transition>
        </div>
    </div>
</template>
 
<style scoped>
    .timer-digit-wrap {
        display: inline-block;
   }

    .timer-digit-container {
        transform-style: preserve-3d;
        height: 1em;
        width: 1ch;
    }

    .timer-digit {
        line-height: 1;
        backface-visibility: hidden;
        position: absolute;
        top: 0;
        left: 0;
        width: 1ch;
    }

    .slide-up-enter-active,
    .slide-up-leave-active {
        transition: all 0.25s ease-out;
    }

    .slide-up-enter-from {
        opacity: 0;
        transform: rotateX(90deg);
        transform: rotateX(-90deg) translateY(-1em);

    }

    .slide-up-leave-to {
        opacity: 0;
        transform: rotateX(-90deg) translateY(1em);
    }
</style>