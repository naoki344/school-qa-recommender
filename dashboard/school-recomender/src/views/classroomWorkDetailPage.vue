<!-- The ref attr used to find the swiper instance -->
<template>
  <v-container>
    <v-card>
      <v-toolbar
        color="yellow darken-1"
        style="max-height: 56px;"
      >
        <v-btn
          icon
          @click="$router.go(-1)"
        >
          <v-icon>mdi-close</v-icon>
        </v-btn>
        <v-toolbar-title>{{ classroom_id }}</v-toolbar-title>
        <v-spacer />
        <v-btn
          icon
          @click="getLatest()"
        >
          <v-icon>mdi-reload</v-icon>
        </v-btn>
      </v-toolbar>
      <v-card-text class="pa-2">
        <v-container
          class="pa-0"
        >
          <div class="split">
            <div class="split-left">
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
                  color="green"
                  text-color="white"
                >
                  {{ question.subject_name }}
                </v-chip>
              </div>
              <div
                class="px-4 pb-4"
                style="display: flex; justify-content: flex-start;"
              >
                <v-chip
                  v-for="tag in question.sort_tag_list"
                  :key="tag"
                  style="margin-right:5px;"
                >
                  {{ tag }}
                </v-chip>
              </div>
              <v-divider class="pb-4" />
              <v-card-text
                id="work-detail-dialog-contents"
                class="px-4 pt-0 pb-6 body-1"
                style="text-align: left;"
              >
                <div v-html="question.question_sentence.contents" />
              </v-card-text>
              <v-divider />
              <v-row style="justify-content: space-around; ">
                <v-col
                  cols="7"
                  md="4"
                  lg="4"
                  class="py-2 px-5"
                >
                  <v-select
                    v-model="selectedTopicId"
                    :items="topicSelectList"
                    :menu-props="{ offsetY: true }"
                    class="font-weight-medium"
                    @change="setDisplayMessageList"
                  >
                    <template v-slot:append-item>
                      <v-divider />
                      <div
                        style="color: blue;"
                        @click="topicCreateDialog = true"
                      >
                        トピックを作成
                      </div>
                    </template>
                  </v-select>
                </v-col>

                <v-col
                  cols="4"
                  class="topic-creator px-0"
                >
                  <div>
                    <v-avatar size="26">
                      <v-img :src="getUserAvatarImageUrl(selectedTopic.register_user_id)" />
                    </v-avatar>
                    <span class="font-weight-black ml-1">{{ selectedTopic.register_user_name }}</span>
                  </div>
                </v-col>
                <v-spacer />
              </v-row>
              <v-divider />

              <div
                v-for="item in topicMessageList"
                :key="item.comment_id"
                class="message-whole ma-3"
              >
                <v-avatar
                  tile
                  style="border-radius: 6px;"
                  size="44"
                >
                  <v-img :src="getUserAvatarImageUrl(item.register_user_id)" />
                </v-avatar>

                <div class="message-area ms-3">
                  <p class="font-weight-bold ma-0 message-contributer-name">
                    {{ item.register_user_name }}
                    <span
                      class="font-weight-medium message-time"
                    >{{ item.register_date | messageTimeSortFilter }}</span>
                  </p>
                  <p class="font-weight-light mb-0 message-body">
                    {{ item.body }}
                  </p>
                </div>
              </div>
            </div>
            <div class="split-right">
              <div class="split-right-inner">
                <div style="height: 10vh;" />
                <p
                  class="mb-1"
                  align="left"
                >
                  {{ selectedTopic.body }}へのコメント
                </p>
                <textarea
                  v-model="editingComment"
                  cols="40"
                  class="textarea"
                  name="editingComment"
                  @keydown.enter.shift.exact="postTopicCommentBody"
                />
                <v-btn
                  block
                  color="yellow darken-1"
                  @click="postTopicCommentBody"
                >
                  投稿する(Shift+Enter)
                </v-btn>
              </div>
            </div>
          </div>
        </v-container>
      </v-card-text>

      <v-card-text style="height: 70px;">
        {{ work_id }}
        {{ classroom_id }}
        <v-btn
          color="pink"
          large
          dark
          fab
          fixed
          bottom
          right
          class="post-comment-btn"
          @click="postCommentDialog = !postCommentDialog"
        >
          <v-icon>mdi-plus</v-icon>
        </v-btn>
      </v-card-text>
    </v-card>

    <v-dialog v-model="postCommentDialog">
      <v-card class="pa-0">
        <v-card-actions>
          <v-btn
            depressed
            icon
            @click="postCommentDialog = false"
          >
            <v-icon>mdi-close</v-icon>
          </v-btn>
          <v-spacer />
          <v-btn
            :disabled="!editingComment"
            color="yellow darken-1"
            @click="postTopicCommentBody"
          >
            投稿する
          </v-btn>
        </v-card-actions>
        <v-divider />
        <v-card-text class="pa-1">
          <v-textarea
            v-model="editingComment"
            autofocus
            solo
            flat
            label="コメントを記入"
          />
        </v-card-text>
      </v-card>
    </v-dialog>
    <v-dialog
      v-model="topicCreateDialog"
      transition="dialog-bottom-transition"
    >
      <v-card>
        <v-card-actions>
          <v-btn
            icon
            @click="topicCreateDialog = false"
          >
            <v-icon>mdi-close</v-icon>
          </v-btn>
          <v-spacer />
          <v-btn
            :disabled="!topicBody"
            color="yellow darken-1"
            @click="postTopic"
          >
            作成する
          </v-btn>
        </v-card-actions>
        <v-card-text>
          <v-text-field
            v-model="topicBody"
            label="トピック名"
            autofocus
          />
        </v-card-text>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script>
import "swiper/dist/css/swiper.css";
import schoolApiQuesionTransfer from "@/api/transfer/question.js";
import moment from "moment";
export default {
  name: "ClassroomWorkDetailPage",
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
    messageTimeSortFilter: function(value) {
      if (!value) return "";
      const currentTime = moment();
      const messageTime = moment(value);
      const yesterday = moment().subtract(1, "day");
      if (messageTime.isSame(currentTime, "day"))
        return messageTime.format("今日 H:m");
      if (messageTime.isSame(yesterday, "day"))
        return messageTime.format("昨日 H:m");
      if (messageTime.isBefore(currentTime))
        return messageTime.format("M月D日 H:m");
    }
  },
  props: {},
  data() {
    return {
      workDetail: { title: "" },
      question: null,
      imageList: [],
      rootMessageList: [],
      topicList: [],
      selectedTopic: { body: "", register_user_name: "", register_user_id: "" },
      topicMessageList: [],
      topicMessageDict: {},
      topicCreateDialog: false,
      rootCommentBody: "",
      topicBody: "",
      selectedTopicId: null,
      postCommentDialog: false,
      editingComment: "",
      editingCommentDict: {},
      work_id: this.$route.query.work_id,
      classroom_id: this.$route.query.classroom_id
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
  mounted() {
    this.$nextTick(function () {
      const contents = document.getElementById('work-detail-dialog-contents');
      const imgList = contents.getElementsByTagName('img');
      imgList.forEach(async img => {
        const url = await this.getImageUrl(img.getAttribute('s3-key'))
        img.setAttribute('src', url);
      })
    })
  },
  beforeMount() {
    this.findClassroomWork();
    this.getWorkCommentList();
  },
  methods: {
    goToBottom() {
      var element = document.documentElement;
      var different = element.scrollHeight - element.clientHeight;
      window.scroll(0, different);
    },
    getLatest() {
      this.findClassroomWork();
      this.getWorkCommentList();
    },
    setDisplayMessageList(comment_id) {
      const beforeCommentId = this.selectedTopic.comment_id;
      if (beforeCommentId !== undefined) {
        this.editingCommentDict[beforeCommentId] = this.editingComment;
      }
      const editingComment = this.editingCommentDict[comment_id];
      if (editingComment !== undefined) {
        this.editingComment = editingComment;
      } else {
        this.editingComment = "";
      }
      this.selectedTopic = this.topicList.find(
        item => item.comment_id === comment_id
      );
      console.log(this.selectedTopic);
      const l = this.topicMessageDict[comment_id];
      if (l != undefined) {
        this.topicMessageList = l;
      } else {
        this.topicMessageList = [];
      }
    },
    findClassroomWork() {
      console.log("questionに代入");
      console.log(this.$route.query.work_id);
      console.log(this.$route.query.classroom_id);
      if (this.$route.query.work_id == null) return;
      if (this.$route.query.classroom_id == null) return;
      const params = {
        classroomId: this.classroom_id,
        workId: this.work_id
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
        if (this.work_id == null) return;
        if (this.classroom_id == null) return;
        const params = {
          classroomId: this.classroom_id,
          workId: this.work_id
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
          classroomId: this.classroom_id,
          workId: this.work_id,
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
      if (!(this.editingComment && this.editingComment.match(/\S/g))) return;
      this.postWorkComment(
        "message",
        this.selectedTopic.comment_id,
        this.editingComment
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
        this.editingComment = "";
        this.postCommentDialog = false;
        this.goToBottom();
      });
    },
    postTopic() {
      this.postWorkComment("topic", null, this.topicBody).then(data => {
        this.topicBody = "";
        this.topicCreateDialog = false;
      });
    },
    async getImageUrl(s3Key) {
      if (s3Key == null) { return null }
      if (this.imageList[s3Key] != null) { return this.imageList[s3Key] }
      const url = await this.$store.dispatch("getS3PublicFile", s3Key)
        .then(async (url) => {
          await this.$set(this.imageList, s3Key, url);
          return this.imageList[s3Key];
        })
        .catch(() => {
          return null;
        });
      return url;
    },
  }
};
</script>

<style lang="scss" scoped>
.message-whole {
  display: flex;
  max-width: 600px;
}
.message-area {
  display: inline-block;
}
.message-contributer-name {
  justify-items: start;
  text-align: left;
  font-family: HiraginoSans-W3;
  font-size: 14px;
}
.message-body {
  white-space: pre-wrap;
  text-align: left;
  font-family: HiraginoSans-W5;
  font-size: 14px;
  line-height: 1.5;
}
.message-time {
  font-size: 70%;
}
.topic-creator {
  display: flex;
  align-items: center;
}
.split {
  display: flex;
}
.split-right {
  display: none;
}

.split-left {
  width: 100%;
}
@media screen and (min-width: 761px) {
  .split-left {
    width: 60%;
  }
  .split-right {
    display: block;
    width: 40%;
  }
  .split-right-inner {
    position: fixed;
    width: 40vw;
    padding-top: 40px;
    padding-left: 25px;
    padding-right: 20px;
    .textarea {
      width: 100%;
      height: 60vh;
      resize: vertical;

      outline: 0;
      border-style: solid;
      color: black;
      background: #fff8e8;
      font-family: HiraginoSans-W4;
      line-height: 1.5;
    }
    .textarea:focus {
      box-shadow: 0 0 7px gray;
      border: 2px solid #fdd836;
    }
  }
  .post-comment-btn {
    display: none;
  }
}
</style>
