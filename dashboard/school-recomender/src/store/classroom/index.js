import schoolApiClient from "@/api/common.js";

export default {
  namespaced: true,
  state: {
      myClassroomList: [],
  },
  mutations: {
    setMyClassroomList(state, data) {
      state.myClassroomList = data;
    }
  },
  actions: {
    fetchMyClassroomList({ commit, rootState }) {
      return new Promise((resolve, reject) => {
        const pathTemplate = '/classroom/my_classroom'
        schoolApiClient
          .fetchRestAPI(
            rootState.cognitoUser,
            "GET",
            pathTemplate,
            {},
            {},
            {}
          )
          .then(result => {
            console.log(result);
            commit("setMyClassroomList", result.data["my_classroom_list"]);
          })
          .catch(() => {
            reject();
          });
      });
    },
  }
}

