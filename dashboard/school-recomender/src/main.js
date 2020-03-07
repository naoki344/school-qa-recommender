import Vue from 'vue'
import App from './App.vue'
import vuetify from './plugins/vuetify';
import store from './store'
import router from './router'
import Amplify, * as AmplifyModules from 'aws-amplify';
import { AmplifyPlugin } from 'aws-amplify-vue'

var cognitoConfig = {
  region: process.env.VUE_APP_REGION,
  userPoolId: process.env.VUE_APP_COGNITO_USER_POOL_ID,
  appClientId: process.env.VUE_APP_COGNITO_APP_CLIENT_ID,
  identifyPoolId: process.env.VUE_APP_IDENTITY_POOL_ID,
  loginsKey: process.env.VUE_APP_LOGINS_KEY
}
// TODO: 全てamplifyに統一する
Amplify.configure({
  Auth: {
      identityPoolId: cognitoConfig.identifyPoolId,
      region: cognitoConfig.region,
      userPoolId: cognitoConfig.userPoolId,
      userPoolWebClientId: cognitoConfig.appClientId
  },
  API: {
    endpoints: [
      {
          name: "ToiToyApi",
          endpoint: process.env.VUE_APP_TOITOY_API_URL
      }
    ]
  },
  Storage: {
    bucket: process.env.VUE_APP_TOITOY_PRIVATE_IMAGE_STORAGE,
    region: process.env.VUE_APP_REGION
  }
});


Vue.config.productionTip = false
Vue.use(AmplifyPlugin, AmplifyModules)

new Vue({
  vuetify,
  store,
  router,
  render: h => h(App)
}).$mount('#app')
