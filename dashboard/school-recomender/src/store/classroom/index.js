import {
  API
} from "aws-amplify";
import Vue from "vue";
import schoolApiClassroomTransfer from "@/api/transfer/classroom.js";

export default {
  namespaced: true,
  state: {
    myClassroomList: null,
    classroomWorkList: {}
  },
  mutations: {
    setMyClassroomList(state, data) {
      state.myClassroomList = data;
    },
    setClassroomWorkList(state, {
      classroom_id,
      work_list
    }) {
      Vue.set(state.classroomWorkList, classroom_id, work_list);
    }
  },
  actions: {
    fetchMyClassroomList({
      commit,
      state,
      dispatch
    }) {
      return new Promise((resolve, reject) => {
        if (state.myClassroomList !== null) {
          resolve();
        }
        API.get(
            "ToiToyApi",
            "/classroom/my_classroom")
          .then(result => {
            const classroom_list = result["my_classroom_list"];
            commit("setMyClassroomList", classroom_list);
            classroom_list.forEach((classroom) => {
              dispatch("fetchClassroomWorkList", classroom.classroom.classroom_id)
                .catch((err) => {
                  reject(err);
                });
            });
            resolve();
          })
          .catch((err) => {
            reject(err);
          });
      });
    },
    fetchClassroom({
      dispatch,
      state
    }, classroomId) {
      return new Promise(async (resolve, reject) => {
        if (state.myClassroomList === null) {
          await dispatch("fetchMyClassroomList")
            .then(result => {
              const classroom = state.myClassroomList.find(classroom => {
                return classroom.classroom.classroom_id == classroomId
              })
              resolve(classroom.classroom)
            })
            .catch((err) => {
              reject(err)
            });
        } else {
          const classroom = state.myClassroomList.find(classroom => {
            return classroom.classroom.classroom_id == classroomId
          })
          resolve(classroom.classroom)
        }
      });
    },
    createInviteLink({
      dispatch,
      state
    }, classroomId) {
      return new Promise(async (resolve, reject) => {
        API.post(
            "ToiToyApi",
            `/classroom/${classroomId}/invite_key`, {
              body: {}
            })
          .then(result => {
            const invite_url = process.env.VUE_APP_TOITOY_PAGE_URL + "invite?inviteKey=" + result.classmate_invite.invite_key;
            resolve({
              "invite_url": invite_url,
              "expire_date": result.classmate_invite.expire_date
            });
          })
          .catch(() => {
            reject();
          });
      });
    },
    fetchClassroomByInviteKey(_, inviteKey) {
      return new Promise((resolve, reject) => {
        API.get(
            "ToiToyApi",
            "/public/invite_key/" + `${inviteKey}/classroom`
          )
          .then(result => {
            resolve(result["classroom"]);
          })
          .catch((e) => {
            reject(e);
          });
      });
    },
    createClassroom({
      dispatch,
      state
    }, inputData) {
      return new Promise(async (resolve, reject) => {
        API.post(
            "ToiToyApi",
            `/classroom`, {
              body: schoolApiClassroomTransfer.toRequest(inputData)
            })
          .then(result => {
            resolve(result);
          })
      });
    },
    modifyClassroom({
      dispatch,
      state
    }, {classroomId, inputData}) {
      return new Promise(async (resolve, reject) => {
        API.put(
            "ToiToyApi",
            `/classroom/${classroomId}`, {
              body: schoolApiClassroomTransfer.toRequest(inputData)
            })
          .then(result => {
            resolve(result);
          })
      });
    },
    fetchClassroomByInviteKey(_, inviteKey) {
      return new Promise((resolve, reject) => {
        API.get(
            "ToiToyApi",
            "/public/invite_key/" + `${inviteKey}/classroom`
          )
          .then(result => {
            resolve(result["classroom"]);
          })
          .catch((e) => {
            reject(e);
          });
      });
    },
    joinRequestByinviteKey(_, inviteKey) {
      return new Promise((resolve, reject) => {
        API.post(
            "ToiToyApi",
            `/invite_key/${inviteKey}/join_request`, {}
          )
          .then(result => {
            resolve();
          })
          .catch((e) => {
            reject(e.response);
          });
      });
    },
    fetchClassroomWorkList({
      commit,
      rootState
    }, classroom_id) {
      return new Promise((resolve, reject) => {
        API.get(
            "ToiToyApi",
            `/classroom/${classroom_id}/work`
          )
          .then(result => {
            commit("setClassroomWorkList", {
              "classroom_id": classroom_id,
              "work_list": result["work_list"]
            });
            resolve();
          })
          .catch((e) => {
            reject(e);
          });
      });
    },
    fetchClassroomWork({
      rootState
    }, {
      classroomId,
      workId
    }) {
      return new Promise((resolve, reject) => {
        API.get(
            "ToiToyApi",
            `/classroom/${classroomId}/work/${workId}`
          )
          .then(result => {
            resolve(result);
          })
          .catch((e) => {
            reject(e);
          });
      });
    },
    getWorkCommentList({
      rootState
    }, {
      classroomId,
      workId
    }) {
      return new Promise((resolve, reject) => {
        API.get(
            "ToiToyApi",
            `/classroom/${classroomId}/work/${workId}/comment`
          )
          .then(result => {
            resolve(result);
          })
          .catch((e) => {
            reject(e);
          });
      });
    },
    approveClassroomJoinRequest({
      rootState
    }, {
      classroomId,
      userId
    }) {
      return new Promise((resolve, reject) => {
        API.put(
            "ToiToyApi",
            `/classroom/${classroomId}/approve_request`, {
              body: {
                approve_user_list: [userId]
              }
            })
          .then(result => {
            resolve(result);
          })
          .catch((e) => {
            reject(e);
          });
      });
    },
    postWorkComment({
      rootState
    }, {
      classroomId,
      workId,
      commentType,
      parentCommentId,
      body
    }) {
      return new Promise((resolve, reject) => {
        const trimmedBody = body.trim();
        API.post(
            "ToiToyApi",
            `/classroom/${classroomId}/work/${workId}/comment`, {
              body: {
                comment_type: commentType,
                parent_comment_id: parentCommentId,
                body: trimmedBody
              }
            })
          .then(result => {
            resolve(result);
          })
          .catch((e) => {
            reject(e);
          });
      });
    },
    registerWork({
      rootState
    }, {
      question,
      selectedClassroom,
      title,
      caption
    }) {
      Promise.all(selectedClassroom.map(async classroomId => {
        return new Promise((resolve, reject) => {
          API.post(
              "ToiToyApi",
              `/classroom/${classroomId}/work`, {
                body: {
                  "question_id": question.question_id,
                  "title": title,
                  "caption": caption
                }
              })
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
