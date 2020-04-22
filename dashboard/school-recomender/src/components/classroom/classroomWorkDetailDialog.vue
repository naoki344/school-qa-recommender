<!-- The ref attr used to find the swiper instance -->
<template>
  <v-container>
    <v-dialog
      v-model="dialogVisible"
      fullscreen
      hide-overlay
      transition="dialog-bottom-transition"
    >
      <v-card>
        <v-toolbar
          color="yellow darken-1"
          style="max-height: 56px;"
        >
          <v-btn
            icon
            @click="closeDialog()"
          >
            <v-icon>mdi-close</v-icon>
          </v-btn>
          <v-toolbar-title>{{ workDetail.title }}</v-toolbar-title>
          <v-spacer />
          <v-btn
            icon
            @click="getLatest()"
          >
            <v-icon>mdi-reload</v-icon>
          </v-btn>
        </v-toolbar>
        <v-divider />
        <v-card-text class="pa-2">
          <v-container
            v-if="question != null"
            class="pa-0"
          >
            <div
              class="px-4 pt-3 pb-2"
              style="display: flex; justify-content: space-between"
            >
              <v-card-title
                class="headline font-weight-bold"
                style="padding: 0;"
              >
                {{ workDetail.title }}
              </v-card-title>
              <v-chip
                small
                :color="question.estimated_time | estimatedColorFilter"
                text-color="white"
                style="padding-left: 6px;"
              >
                {{ question.subject_type | subjectTypeFilter }}
              </v-chip>
            </div>
            <div
              class="px-4 pb-4"
              style="display: flex; justify-content: letf"
            >
              {{ tag }}
            </div>
            <v-divider class="pb-4" />
            <v-card-text
              class="px-4 pt-0 pb-6 body-1"
              style="text-align: left;"
            >
              {{ question.question_sentence.text }}
            </v-card-text>
            <v-img
              v-if="getImageUrl(question.question_sentence)"
              class="mb-2"
              :src="imageList[question.question_sentence.image_url]"
              style="width: 100%;"
            />
            <v-divider />

            <v-col cols="6">
              <v-select
                v-model="prefixTopic"
                :items="topicSelectList"
                :menu-props="{ offsetY: true }"
                @change="setDisplayMessageList"
              >
                <template v-slot:append-item>
                  <v-divider />
                  <div
                    style="color: blue;"
                    @click="topicCreateDialog = true"
                  >
                    新しいトピックを作成する
                  </div>
                </template>
              </v-select>
            </v-col>

            <v-divider />
            <v-list three-line>
              <template v-for="item in topicMessageList">
                <v-list-item :key="item.comment_id">
                  <v-list-item-avatar tile>
                    <v-img
                      :src="getUserAvatarImageUrl(item.register_user_id)"
                    />
                  </v-list-item-avatar>

                  <v-list-item-content>
                    <v-list-item-title>
                      <p style="text-align: left">
                        {{ item.register_user_name }}
                      </p>
                    </v-list-item-title>
                    <v-list-item-subtitle>
                      <p style="text-align: left">
                        {{ item.body }}
                      </p>
                    </v-list-item-subtitle>
                  </v-list-item-content>
                </v-list-item>
              </template>
              <v-textarea
                v-model="rootCommentBody"
                label="Leave a comment..."
                solo
              />
              <div style="display: flex;">
                <v-spacer />
                <v-btn
                  class="mx-0"
                  depressed
                  @click="postRootCommentBody"
                >
                  Post1
                </v-btn>
              </div>
            </v-list>
          </v-container>
        </v-card-text>
      </v-card>
    </v-dialog>
    <v-dialog
      v-model="topicCreateDialog"
      hide-overlay
      transition="dialog-bottom-transition"
    >
      <v-card class="pa-0">
        <v-card-title>新しいトピックを作成する</v-card-title>
        <v-divider />
        <v-card-text>
          <v-textarea
            v-model="topicBody"
            label="Leave a comment..."
            solo
          />
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn
            class="mx-0"
            depressed
            @click="postTopic"
          >
            Post3
          </v-btn>
          <v-btn
            color="primary"
            text
            @click="topicCreateDialog = false"
          >
            閉じる
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script>
import "swiper/dist/css/swiper.css";
import schoolApiQuesionTransfer from "@/api/transfer/question.js";
import moment from "moment";
export default {
  name: "ClassroomWorkDetail",
  components: {},
  filters: {
    subjectTypeFilter: function(value) {
      if (value == null) return "";
      if (!value) return "";
      return schoolApiQuesionTransfer.getSubjectNameFromType(value);
    },
    questionTypeFilter: function(value) {
      if (value == null) return "";
      if (!value) return "";
      if (value === "describing") return "記述式";
      if (value === "selectable") return "選択式";
      return "";
    },
    dateTimeFilter: function(value) {
      if (value == null) return "";
      if (!value) return "";
      return moment(value).format("MM月DD日 hh:mm");
    },
    estimatedColorFilter: function(value) {
      if (value == null) return "";
      if (!value) return "green";
      if (value <= 1) return "blue";
      if (value <= 5) return "green";
      if (value <= 15) return "orange";
      if (value > 15) return "red";
    }
  },
  props: {
    dialogVisible: {
      type: Boolean,
      required: true
    },
    work: {
      type: [String, Object],
      required: true
    },
    classroom: {
      type: [String, Object],
      required: true
    }
  },
  data() {
    return {
      workDetail: { title: "" },
      question: null,
      imageList: [],
      rootMessageList: [],
      topicList: [],
      selectedTopic: { body: "", register_user_name: "" },
      topicMessageList: [],
      topicMessageDict: {},
      topicCreateDialog: false,
      rootCommentBody: "",
      topicCommentBody: "",
      topicBody: "",
      prefixTopic: "test"
    };
  },
  computed: {
    topicSelectList() {
      const msgList = this.topicList.map(topic => {
        let body = topic.body;
        if (body == null || body == undefined) {
          body = "タイトルなし";
        }
        return {
          text: body,
          value: topic.comment_id
        };
      });

      return msgList;
    }
  },
  watch: {
    work() {
      this.findClassroomWork();
      this.getWorkCommentList();
    }
  },
  methods: {
    closeDialog() {
      this.$emit("closeDialog");
    },
    getLatest() {
      this.findClassroomWork();
      this.getWorkCommentList();
    },

    setDisplayMessageList(comment_id) {
      const l = this.topicMessageDict[comment_id];
      if (l != undefined) {
        this.topicMessageList = l;
      } else {
        this.topicMessageList = [];
      }
    },
    findClassroomWork() {
      if (this.work == null) return;
      if (this.classroom == null) return;
      const params = {
        classroomId: this.classroom.classroom_id,
        workId: this.work.work_id
      };
      this.$store
        .dispatch("classroom/fetchClassroomWork", params)
        .then(data => {
          this.workDetail = data["work"];
          this.question = data["question"];
          this.commentList = data["comment_list"];
        })
        .catch(err => {
          console.log(err);
        });
    },
    getWorkCommentList() {
      return new Promise((resolve, reject) => {
        if (this.work == null) return;
        if (this.classroom == null) return;
        const params = {
          classroomId: this.classroom.classroom_id,
          workId: this.work.work_id
        };
        this.$store
          .dispatch("classroom/getWorkCommentList", params)
          .then(data => {
            this.topicList = data["topic_list"];
            this.rootMessageList = data["root_message_list"];
            this.topicMessageDict = data["topic_message_dict"];
            resolve(data);
          })
          .catch(err => {
            console.log(err);
            reject(err);
          });
      });
    },
    postWorkComment(commentType, parentCommentId, body) {
      return new Promise((resolve, reject) => {
        if (this.work == null) return;
        if (this.classroom == null) return;
        const params = {
          classroomId: this.classroom.classroom_id,
          workId: this.work.work_id,
          commentType,
          parentCommentId,
          body
        };
        this.$store
          .dispatch("classroom/postWorkComment", params)
          .then(data => {
            this.getWorkCommentList()
              .then(data => {
                resolve(data);
              })
              .catch(err => {
                reject(err);
              });
          })
          .catch(err => {
            alert("コメントの登録に失敗しました");
            reject(err);
          });
      });
    },
    postRootCommentBody() {
      this.postWorkComment("message", null, this.rootCommentBody).then(data => {
        this.rootCommentBody = "";
      });
    },
    getUserAvatarImageUrl(userId) {
      return this.$store.getters["user/userAvatarImageUrl"](userId);
    },
    postTopicCommentBody() {
      this.postWorkComment(
        "message",
        this.selectedTopic.comment_id,
        this.topicCommentBody
      ).then(data => {
        const topicMessage = this.topicMessageDict[
          this.selectedTopic.comment_id
        ];
        console.log("test");
        console.log(topicMessage);
        if (topicMessage instanceof Array) {
          console.log(this.topicMessageList);
          this.topicMessageList.splice(
            0,
            this.topicMessageList.length,
            ...topicMessage
          );
        } else {
          this.topicMessageList.splice(0, this.topicMessageList.length, [data]);
        }
        this.topicCommentBody = "";
      });
    },
    postTopic() {
      this.postWorkComment("topic", null, this.topicBody).then(data => {
        this.topicBody = "";
        this.topicCreateDialog = false;
      });
    },
    getImageUrl(obj) {
      if (obj["image_url"] == null) {
        return false;
      }
      const path = obj["image_url"];
      if (this.imageList[path] != null) {
        return true;
      }
      this.$store
        .dispatch("getS3PublicFile", path)
        .then(url => {
          this.$set(this.imageList, path, url);
        })
        .catch(() => {
          return false;
        });
      return true;
    }
  }
};
</script>
