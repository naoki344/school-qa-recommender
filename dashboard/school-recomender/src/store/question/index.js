import {
  API
} from "aws-amplify";
import schoolApiQuesionTransfer from "@/api/transfer/question.js";

export default {
  namespaced: true,
  state: {
    questionCardList: []
  },
  mutations: {
    setQuestionCardList(state, data) {
      state.questionCardList = data;
    }
  },
  actions: {
    fetchQuestionList({
      commit,
      rootState
    }) {
      API.get(
          "ToiToyApi",
          "/question")
        .then(result => {
          commit("setQuestionCardList", result["question_card_list"]);
        });
    },
    fetchQuestion({
      rootState
    }, questionId) {
      return new Promise((resolve, reject) => {
        API.get(
            "ToiToyApi",
            `/question/${questionId}`)
          .then(result => {
            resolve(result);
          })
          .catch(err => {
            alert("API連携エラー", err);
            console.log(err);
            reject();
          });
      });
    },
    createQuestion({
      rootState
    }, {
      questionInput
    }) {
      return new Promise((resolve, reject) => {
        API.post(
            "ToiToyApi",
            "/question", {
              body: schoolApiQuesionTransfer.toRequest(questionInput)
            })
          .then(() => {
            alert("登録に成功しました");
            resolve();
          })
          .catch(err => {
            alert("API連携エラー", err);
            console.log(err);
            reject();
          });
      });
    },
    modifyClassroom({
      dispatch,
      state
    }, {
      questionId,
      inputData
    }) {
      return new Promise(async (resolve, reject) => {
        API.put(
            "ToiToyApi",
            `/question/${questionId}`, {
              body: schoolApiQuesionTransfer.toRequest(inputData)
            })
          .then(result => {
            resolve(result);
          })
      });
    }
  },
}