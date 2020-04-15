import schoolApiClient from "@/api/common.js";

export default {
  namespaced: true,
  state: {
    loginUser: schoolApiClient.getCurrentUser(),
    registeredUser: {}
  },
  mutations: {
    setLoginUser(state, data) {
      state.loginUser = data;
    },
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
    async userSignUp({ commit }, inputData) {
      try {
        if (inputData.avatarImageDataUrl != '') {
          const res = await schoolApiClient.publicApiPutClient(
              "/public/user/avatar",
              inputData.avatarImageDataUrl)
          inputData["avatarUrl"] = res["avatar_url"]
        }
        const cognitoUser = await schoolApiClient.userSignUp(inputData)
      } catch(err) {
        throw new Error(err)
      }
    }
  }
};
