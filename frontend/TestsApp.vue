<script setup lang="ts">
  import { ref } from 'vue';

  import DigitWheel from './components/DigitWheel.vue'
  import SidebarScrollingTitle from './components/SidebarScrollingTitle.vue'

  const counter = ref(1);
  const sidebar_scrolling_title = ref();
  const text_sidebar = ref("ROUND");

  window.setInterval(() => {
    counter.value += 1
  }, 1000)

  function changeSiderbarProp() {
    if (text_sidebar.value == "ZIZI") {
      text_sidebar.value = "ROUND";
    } else {
      text_sidebar.value = "ZIZI";
    }
  }
</script>

<template>
  <DigitWheel :num="counter" id="da-wheel" />
  <SidebarScrollingTitle ref="sidebar_scrolling_title" :text="text_sidebar" />
  <div style="position: absolute; top: 300px; right: 0;">
    <SidebarScrollingTitle ref="sidebar_scrolling_title" side="right" :text="text_sidebar"/>
  </div>

  <button type="button" @click="changeSiderbarProp" style="position: absolute; bottom: 0px; left: 0%; width: 100px; height: 50px;">
    changeSiderbarProp
  </button>
</template>

<style scoped>
  #da-wheel {
    font-size: 12em;
  }
</style>
