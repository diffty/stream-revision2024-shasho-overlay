import{d as D,r as o,O as W,w as g,o as a,c as r,a as t,b as N,e as R,t as d,T as y,j as _,p as B,g as x,_ as V,h as P,S as $,i as j}from"./_plugin-vue_export-helper-CEF5PBLk.js";const c=p=>(B("data-v-fd977e2c"),p=p(),x(),p),L={id:"title",class:"slight-tilting"},U={id:"title-line1",class:"slight-moving"},M={key:0,id:"title-line1-stage2",class:"title-stage-line"},G={key:1,id:"title-line1-stage3",class:"title-stage-line"},H={key:2,id:"title-line1-stage1",class:"title-stage-line"},J={id:"title-line2",class:"slight-moving-reverse"},Y={key:0,id:"title-line2-stage2",class:"title-stage-line"},F=c(()=>t("br",null,null,-1)),q=c(()=>t("br",null,null,-1)),z=c(()=>t("br",null,null,-1)),K=c(()=>t("br",null,null,-1)),Q={key:1,id:"title-line2-stage3",class:"title-stage-line"},X=c(()=>t("br",null,null,-1)),Z=c(()=>t("span",{class:"small-versus"},"VS",-1)),ee=c(()=>t("br",null,null,-1)),te=c(()=>t("span",{class:"small-versus"},"VS",-1)),se={key:2,id:"title-line2-stage1",class:"title-stage-line"},A="ws://localhost:4455",m="ws://localhost:6969",ne="http://localhost:8080",oe="meubapelefoute",ae=D({__name:"RevisionIntroSplash",async setup(p){let s,l;const v=o("INTRO");var S=!1;const O=o(""),E=o(""),w=o(""),f=o(""),b=o(""),I=o(""),T=o("");var n;function C(e){v.value=e}async function k(){const e=await fetch(`${ne}/current_round`).catch(i=>{console.error(`Can't retrieve current round infos : ${i}`)});e&&e.status==200&&(console.log("Config loaded!"),n=await e.json(),O.value=n.round.coders[0],E.value=n.round.coders[1],w.value=n.round.coders[2],f.value=n.roundName,b.value=n.round.djName,I.value=n.round.commentsName,T.value=n.hostName)}const h=new WebSocket(m);h.addEventListener("open",()=>{console.log(`Connected to server ${m}.`)}),h.addEventListener("error",e=>{console.error(`Error with the server Websocket connection ${m}`)}),h.addEventListener("close",e=>{console.error(`Websocket connection with server ${m} closed.`)}),h.addEventListener("message",e=>{const i=JSON.parse(e.data);switch(i.type){case"ConfigEvent":i.payload.doUpdate&&k();break}});const u=new W;if([s,l]=g(()=>u.connect(A,oe).then(()=>{S=!0}).catch(()=>{console.error(`Can't connect to OBS websockets ${A}`)})),await s,l(),u.on("SceneTransitionStarted",async function(e){const i=await u.call("GetCurrentProgramScene");C(i.currentProgramSceneName)}),u.on("ConnectionError",()=>{S=!1}),u.on("ConnectionClosed",()=>{S=!1}),[s,l]=g(()=>k()),await s,l(),S){const e=([s,l]=g(()=>u.call("GetCurrentProgramScene")),s=await s,l(),s);C(e.sceneName)}return(e,i)=>(a(),r("div",L,[t("div",U,[N(y,{name:"slide-down-up"},{default:R(()=>[v.value==="INTRO_ROUND"?(a(),r("span",M,d(f.value),1)):v.value==="INTRO_VS"?(a(),r("span",G,d(f.value),1)):(a(),r("span",H,"SHADER"))]),_:1})]),t("div",J,[N(y,{name:"slide-up-down"},{default:R(()=>[v.value==="INTRO_ROUND"?(a(),r("span",Y,[_(" COMMENTARIES "),F,_(d(I.value),1),q,_(" DJ SET "),z,_(d(b.value),1),K])):v.value==="INTRO_VS"?(a(),r("span",Q,[_(d(O.value),1),X,Z,_(" "+d(E.value),1),ee,te,_(" "+d(w.value),1)])):(a(),r("span",se,"SHOWDOWN"))]),_:1})])]))}}),ce=V(ae,[["__scopeId","data-v-fd977e2c"],["__file","/Users/diffty/_Projets/Streaming/2024_04_Revision2024/OVERLAY/src/components/RevisionIntroSplash.vue"]]),le=D({__name:"RevisionIntroSplashApp",setup(p){return(s,l)=>(a(),P($,null,{default:R(()=>[N(ce)]),_:1}))}}),ie=V(le,[["__file","/Users/diffty/_Projets/Streaming/2024_04_Revision2024/OVERLAY/src/RevisionIntroSplashApp.vue"]]);j(ie).mount("#app");
