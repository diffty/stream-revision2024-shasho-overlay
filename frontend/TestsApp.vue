<script setup lang="ts">
  import { ref } from 'vue';

  import DigitWheel from './components/DigitWheel.vue'

  const counter = ref(1);

  window.setInterval(() => {
    counter.value += 1
  }, 1000)
</script>

<template>
  <Suspense>
    <DigitWheel :num="counter" id="da-wheel" />
  </Suspense>
</template>

<style scoped>
  #da-wheel {
    font-size: 12em;
  }
</style>
