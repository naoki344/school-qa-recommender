import userStore from "@/store/user/index.js";
import questionStore from "@/store/question/index.js";
import classroomStore from "@/store/classroom/index.js";
import { Storage } from "aws-amplify";

import Vue from "vue";
import Vuex from "vuex";

Vue.use(Vuex);

export default new Vuex.Store({
  modules: {
    user: userStore,
    question: questionStore,
    classroom: classroomStore,
  },
  actions: {
    getS3PublicFile(_, filePath) {
      return new Promise((resolve, reject) => {
        Storage.configure({ level: "public" });
        Storage.get(filePath, { expires: 3600 })
          .then((url) => {
            resolve(url);
          })
          .catch(err => {
            alert("画像取得エラー", err);
            reject();
          });
      });
    },
    putS3PublicFile(_, {file}) {
      return new Promise((resolve, reject) => {
        const dt = new Date();
        const filePath = dt.getTime() + "-" + file.name;
        Storage.configure({ level: "public" });
        Storage.put("" + filePath, file)
          .then((result) => {
            resolve(result);
          })
          .catch(err => {
            alert("画像アップロードに失敗しました", err);
            reject();
          });
      });
    },
  }
});
