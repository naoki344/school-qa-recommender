import schoolApiClient from "@/api/common.js";
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
    fetchQuestionList({ commit, rootState }) {
      const pathTemplate = '/question'
      const pathParams = {};
      schoolApiClient
        .fetchRestAPI(
          "GET",
          pathTemplate,
          pathParams,
          {},
          {}
        )
        .then(result => {
          commit("setQuestionCardList", result.data["question_card_list"]);
        });
    },
    fetchQuestion({ rootState }, questionId) {
      return new Promise((resolve, reject) => {
        const pathTemplate = '/question/{questionId}'
        const pathParams = {questionId: questionId};
        schoolApiClient
          .fetchRestAPI(
            "GET",
            pathTemplate,
            pathParams,
            {},
            {}
          )
          .then(result => {
            resolve(result.data);
          })
          .catch(err => {
            alert("API連携エラー", err);
            console.log(err);
            reject();
          });
        });
    },
    createQuestion({ rootState }, { questionInput }) {
      return new Promise((resolve, reject) => {
        const data = schoolApiQuesionTransfer.toRequest(questionInput);
        console.log(data);
        const pathTemplate = '/question'
        schoolApiClient
          .fetchRestAPI(
            "POST",
            pathTemplate,
            {},
            {},
            data
          )
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
    }
  },
}
