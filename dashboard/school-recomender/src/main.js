import Vue from 'vue'
import App from './App.vue'
import vuetify from './plugins/vuetify';
import store from './store'
import router from './router'
import VueQriously from "vue-qriously";
import Amplify, * as AmplifyModules from 'aws-amplify';
import {
  AmplifyPlugin
} from 'aws-amplify-vue'

var cognitoConfig = {
  region: process.env.VUE_APP_REGION,
  userPoolId: process.env.VUE_APP_COGNITO_USER_POOL_ID,
  appClientId: process.env.VUE_APP_COGNITO_APP_CLIENT_ID,
  identifyPoolId: process.env.VUE_APP_IDENTITY_POOL_ID,
  loginsKey: process.env.VUE_APP_LOGINS_KEY
}
Amplify.configure({
  Auth: {
    identityPoolId: cognitoConfig.identifyPoolId,
    region: cognitoConfig.region,
    userPoolId: cognitoConfig.userPoolId,
    userPoolWebClientId: cognitoConfig.appClientId
  },
  API: {
    endpoints: [{
      name: "ToiToyApi",
      endpoint: process.env.VUE_APP_TOITOY_API_URL,
      region: "ap-northeast-1",
    }]
  },
  Storage: {
    bucket: process.env.VUE_APP_TOITOY_PRIVATE_IMAGE_STORAGE,
    region: process.env.VUE_APP_REGION
  }
});


Vue.config.productionTip = false
Vue.use(AmplifyPlugin, AmplifyModules)
Vue.use(VueQriously);

new Vue({
  vuetify,
  store,
  router,
  render: h => h(App)
}).$mount('#app')