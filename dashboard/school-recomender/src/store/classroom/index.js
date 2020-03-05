import schoolApiClient from "@/api/common.js";

export default {
  namespaced: true,
  state: {
      classroomList: [],
  },
  mutations: {
    setClassroomList(state, data) {
      state.classroomList = data;
    }
  },
  actions: {
    fetchClassroomList({ commit, rootState }) {
      return new Promise((resolve, reject) => {
        const pathTemplate = '/classroom/{classroomId}'
        const pathParams = {"classroomId": "3"};
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
            console.log(result);
            commit("setClassroomList", [result.data["classroom"], result.data["classroom"]]);
          })
          .catch(() => {
            reject();
          });
      });
    },
  }
}

