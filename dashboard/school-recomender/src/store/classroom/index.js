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
    fetchClassroomWork({ rootState }, { classroomId, workId }) {
      return new Promise((resolve, reject) => {
        const pathTemplate = '/classroom/{classroom_id}/work/{work_id}'
        schoolApiClient
          .fetchRestAPI(
            "GET",
            pathTemplate,
            {"classroom_id": classroomId, "work_id": workId},
            {},
            {}
          )
          .then(result => {
            resolve(result.data);
          })
          .catch((e) => {
            reject(e);
          });
      });
    },
    getWorkCommentList({ rootState }, { classroomId, workId }) {
      return new Promise((resolve, reject) => {
        const pathTemplate = '/classroom/{classroom_id}/work/{work_id}/comment'
        schoolApiClient
          .fetchRestAPI(
            "GET",
            pathTemplate,
            {"classroom_id": classroomId, "work_id": workId},
            {},
            {}
          )
          .then(result => {
            resolve(result.data);
          })
          .catch((e) => {
            reject(e);
          });
      });
    },
    postWorkComment({ rootState }, { classroomId, workId, commentType, parentCommentId, body }) {
      return new Promise((resolve, reject) => {
        const pathTemplate = '/classroom/{classroom_id}/work/{work_id}/comment'
        schoolApiClient
          .fetchRestAPI(
            "POST",
            pathTemplate,
            {"classroom_id": classroomId, "work_id": workId},
            {},
            {comment_type: commentType, parent_comment_id: parentCommentId, body: body}
          )
          .then(result => {
            resolve(result.data);
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

