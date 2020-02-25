import schoolApiClient from '../api/common.js';
import schoolApiQuesionTransfer from '../api/transfer/question.js';
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
      return new Promise((resolve, reject) => {
        schoolApiClient.userLogin(state.cognitoConfig, {
          Username: username,
          Password: password
        }).then((cognitoUser) => {
          commit('setLoginUser', cognitoUser);
          resolve()
        }).catch(() => {
          reject()
        });
      });
    },
    userSignUp({commit, state}, inputData) {
      return new Promise((resolve, reject) => {
        schoolApiClient.userSignUp(state.cognitoConfig, inputData)
        .then((cognitoUser) => {
          commit('setLoginUser', cognitoUser);
          resolve()
        }).catch(() => {
          reject()
        });
      });
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
      return new Promise((resolve, reject) => {
        const data = schoolApiQuesionTransfer.toRequest(questionInput)
        console.log(data);
        const pathTemplate = '/devmiyoshi/admin/question'
        schoolApiClient.fetchRestAPI(
          state.cognitoConfig, state.cognitoUser, "POST", pathTemplate, {}, {}, data
        ).then(() => {
          alert("登録に成功しました");
          resolve()
        }).catch((err) => {
          alert("API連携エラー", err);
          console.log(err);
          reject()
        });
      });
    }
  },
  modules: {
  }
})
