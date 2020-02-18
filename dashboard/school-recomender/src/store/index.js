import schoolApiClient from '../api/common.js';
import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
	loginUser: {},
    cognitoConfig: {
      region: process.env.VUE_APP_REGION,
      userPoolId: process.env.VUE_APP_COGNITO_USER_POOL_ID,
      appClientId: process.env.VUE_APP_COGNITO_APP_CLIENT_ID,
      adminIdentifyPoolId: process.env.VUE_APP_ADMIN_IDENTITY_POOL_ID,
      adminLoginsKey: process.env.VUE_APP_ADMIN_LOGINS_KEY
    },
    questionCardList: []
  },
  mutations: {
    setLoginUser(state, data) {
      state.loginUser = data;
    },
    setQuestionCardList(state, data) {
      state.questionCardList = data;
    },
  },
  actions: {
    userLogin({commit, state}, {username, password}) {
      const cognitoUser = schoolApiClient.loginUser(state.cognitoConfig, {
        Username: username,
        Password: password
      });
      commit('setLoginUser', cognitoUser);
    },
    fetchQuestionList({commit, state}) {
      const pathTemplate = '/devmiyoshi/admin/question'
      const pathParams = {};
      schoolApiClient.fetchRestAPI(
        state.cognitoConfig, state.cognitoUser, "GET", pathTemplate, pathParams, {}, {}
      ).then((result) => {
        commit('setQuestionCardList', result.data["question_card_list"]);
      });
    },
    createQuestion({state}, {questionInput}) {
      console.log(questionInput);
      const pathTemplate = '/devmiyoshi/admin/question'
      schoolApiClient.fetchRestAPI(
        state.cognitoConfig, state.cognitoUser, "GET", pathTemplate, {}, {}, {}
      ).then((result) => {
        console.log(result);
      });
    }
  },
  modules: {
  }
})
