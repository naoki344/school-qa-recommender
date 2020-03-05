import userStore from "@/store/user/index.js";
import schoolApiClient from "@/api/common.js";
import questionStore from "@/store/question/index.js";

import Vue from "vue";
import Vuex from "vuex";

Vue.use(Vuex);

export default new Vuex.Store({
  modules: {
    user: userStore,
    question: questionStore
  },
  actions: {
    getS3PublicFile(_, filePath) {
      return new Promise((resolve, reject) => {
        schoolApiClient
          .getS3PublicFile(filePath)
          .then((url) => {
            resolve(url);
          })
          .catch(err => {
            alert("画像取得エラー", err);
            reject();
          });
      });
    }
  }
});
