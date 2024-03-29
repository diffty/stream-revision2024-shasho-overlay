import { createApp, ref } from 'vue'
import App from './RevisionIntroSplash.vue'

createApp(App).mount('#app')

const queryString = window.location.search;
const urlParams = new URLSearchParams(queryString);

const invertColorsArg = urlParams.get("invertcolors");

if (invertColorsArg != null) {
    document.documentElement.classList.add('invertColors');
}
