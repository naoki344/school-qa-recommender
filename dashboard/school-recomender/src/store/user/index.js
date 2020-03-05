import schoolApiClient from "@/api/common.js";

const store = {
  namespaced: true,
  state: {
      loginUser: {},
  },
  mutations: {
    setLoginUser(state, data) {
      state.loginUser = data;
    }
  },
  actions: {
    userLogin({ commit }, { username, password }) {
      return new Promise((resolve, reject) => {
        schoolApiClient
          .userLogin(username, password)
          .then(cognitoUser => {
            commit("setLoginUser", cognitoUser);
            resolve();
          })
          .catch(() => {
            reject();
          });
      });
    },
    userVerify(_, { email, verificationCode }) {
      return new Promise((resolve, reject) => {
        schoolApiClient
          .userVerify({
            email: email,
            verificationCode: verificationCode
          })
          .then(() => {
            resolve();
          })
          .catch(() => {
            reject();
          });
      });
    },
    userSignUp({ commit }, inputData) {
      return new Promise((resolve, reject) => {
        schoolApiClient
          .userSignUp(inputData)
          .then(cognitoUser => {
            commit("setLoginUser", cognitoUser);
            resolve();
          })
          .catch(() => {
            reject();
          });
      });
    },
  }
}

export default store
