import schoolApiClient from "@/api/common.js";
import Vue from "vue";

export default {
  namespaced: true,
  state: {
      myClassroomList: [],
      classroomWorkList: {},
  },
  mutations: {
    setMyClassroomList(state, data) {
      state.myClassroomList = data;
    },
    setClassroomWorkList(state, {classroom_id, work_list}) {
      Vue.set(state.classroomWorkList, classroom_id, work_list);
    }
  },
  actions: {
    fetchMyClassroomList({ commit, rootState, dispatch }) {
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
            const classroom_list = result.data["my_classroom_list"];
            commit("setMyClassroomList", classroom_list);
            classroom_list.forEach((classroom) => {
              dispatch("fetchClassroomWorkList", classroom.classroom.classroom_id)
                .catch((err) => {
                  console.log(err);
                });
            })
          })
          .catch((err) => {
            console.log(err);
            reject(err);
          });
      });
    },
    fetchClassroomWorkList({ commit, rootState }, classroom_id) {
      return new Promise((resolve, reject) => {
        const pathTemplate = '/classroom/{classroom_id}/work'
        schoolApiClient
          .fetchRestAPI(
            rootState.cognitoUser,
            "GET",
            pathTemplate,
            {"classroom_id": classroom_id},
            {},
            {}
          )
          .then(result => {
            commit("setClassroomWorkList", {"classroom_id": classroom_id, "work_list": result.data["work_list"]});
            resolve();
          })
          .catch((e) => {
            reject(e);
          });
      });
    },
    registerWork({ rootState }, {question, selectedClassroom, title, caption}) {
      const pathTemplate = '/classroom/{classroom_id}/work'
      Promise.all(selectedClassroom.map(async classroomId => {
        return new Promise((resolve, reject) => {
          schoolApiClient
            .fetchRestAPI(
              rootState.cognitoUser,
              "POST",
              pathTemplate,
              {"classroom_id": classroomId},
              {},
              {"question_id": question.question_id, "title": title, "caption": caption}
            )
            .then(result => {
              resolve(result);
            })
            .catch(() => {
              reject();
            });
        })
      }))
    },
  }
}

