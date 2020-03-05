import schoolApiClient from "@/api/common.js";
import schoolApiQuesionTransfer from "@/api/transfer/question.js";

const store = {
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
          rootState.cognitoUser,
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
    createQuestion({ rootState }, { questionInput }) {
      return new Promise((resolve, reject) => {
        const data = schoolApiQuesionTransfer.toRequest(questionInput);
        console.log(data);
        const pathTemplate = '/question'
        schoolApiClient
          .fetchRestAPI(
            rootState.cognitoUser,
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

export default store
