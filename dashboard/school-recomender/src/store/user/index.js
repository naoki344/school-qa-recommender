import axios from "axios";
import { Auth } from "aws-amplify";

const userApiClient = {
  userSignUp(inputData) {
    return new Promise((resolve, reject) => {
      let attributes = {
        email: inputData.email,
        nickname: inputData.nickname,
        "custom:last_name": inputData.lastName,
        "custom:first_name": inputData.firstName,
        "custom:last_name_kana": inputData.lastNameKana,
        "custom:first_name_kana": inputData.firstNameKana
      };
      if (inputData.avatarUrl != null) {
        attributes = {
          ...attributes,
          "custom:avatar_url": inputData.avatarUrl
        };
      }
      Auth.signUp({
        username: inputData.email,
        password: inputData.password,
        attributes: attributes
      })
        .then(() => {
          resolve();
        })
        .catch(err => {
          console.log(err)
          console.log(err.message)
          reject(err);
        });
    });
  },
  publicApiPutClient(path, data) {
    return new Promise((resolve, reject) => {
      const api = axios.create({
        baseURL: process.env.VUE_APP_TOITOY_API_URL
      });
      console.log(path);
      api
        .put(path, data)
        .then(response => {
          resolve(response.data);
        })
        .catch(err => {
          console.log(err);
          reject("ユーザー画像のアップロードに失敗しました");
        });
    });
  }
};

export default {
  namespaced: true,
  state: {
    loginUser: null,
    registeredUser: {}
  },
  mutations: {
    setLoginUser(state, data) {
      state.loginUser = data;
    }
  },
  getters: {
    userAvatarImageUrl: state => userId => {
      return `${process.env.VUE_APP_TOITOY_PUBLIC_IMAGE_STORAGE_URL}/user/${userId}/avatar_image`;
    }
  },
  actions: {
    userLogin({ commit }, { username, password }) {
      return new Promise((resolve, reject) => {
        Auth.signIn(username, password)
          .then(cognitoUser => {
            commit("setLoginUser", cognitoUser);
            resolve();
          })
          .catch(err => {
            reject(err);
          });
      });
    },
    userLogout({ commit }) {
      return new Promise((resolve, reject) => {
        Auth.signOut()
          .then(() => {
            commit("setLoginUser", undefined);
            resolve();
          })
          .catch(err => {
            reject(err);
          });
      });
    },
    userVerify(_, { email, verificationCode }) {
      return new Promise((resolve, reject) => {
        Auth.confirmSignUp(email, verificationCode)
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
        if (inputData.avatarImageDataUrl != "") {
          const res = await userApiClient.publicApiPutClient(
            "/public/user/avatar",
            inputData.avatarImageDataUrl
          );
          inputData["avatarUrl"] = res["avatar_url"];
        }
        const cognitoUser = await userApiClient.userSignUp(inputData);
      } catch (err) {
        throw new Error(err);
      }
    },
    fetchLoginUserInfo({ commit }) {
      return new Promise((resolve, reject) => {
        Auth.currentAuthenticatedUser()
          .then(user => {
            commit("setLoginUser", user);
          })
          .catch(() => {
            commit("setLoginUser", undefined);
          });
      });
    },
    fetchMyAvatarImageUrl({ commit, state }) {
      const userId = state.loginUser.attributes["custom:avatar_url"];
      if (userId === undefined) {
        return "";
      }
      return userId;
    }
  }
};
