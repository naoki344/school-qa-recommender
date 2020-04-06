<!-- The ref attr used to find the swiper instance -->
<template>
  <v-container>
    <v-dialog
      v-model="dialogVisible"
      fullscreen
      hide-overlay
      transition="dialog-bottom-transition"
      scrollable
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
                {{ question.subject_type | subjectTypeFilter }}
              </v-card-title>
              <v-chip
                class
                small
                :color="question.estimated_time | estimatedColorFilter"
                text-color="white"
                style="padding-left: 6px;"
              >
                <v-avatar
                  left
                  :class="question.estimated_time | estimatedColorFilter"
                  class="darken-4"
                >
                  {{ question.estimated_time }}
                </v-avatar>Min
              </v-chip>
            </div>
            <div
              class="px-4 pb-4"
              style="display: flex; justify-content: letf"
            >
              <v-chip
                v-for="(tag, index) in question.sort_tag_list"
                :key="index"
                style="margin-right:5px;"
              >
                {{ tag }}
              </v-chip>
            </div>
            <v-divider class="pb-4" />
            <v-card-text
              class="pb-2 px-4 title"
              style="text-align: left;"
            >
              ＜問い＞
            </v-card-text>
            <v-img
              v-if="getImageUrl(question.question_sentence)"
              class="mb-2"
              :src="imageList[question.question_sentence.image_url]"
              style="width: 100%;"
            />
            <v-card-text
              class="px-4 pt-0 pb-6 body-1"
              style="text-align: left;"
            >
              {{ question.question_sentence.text }}
            </v-card-text>
            <v-divider />
            <v-list
              two-line
              subheader
              style="text-align: left;"
            >
              <v-subheader>
                トピック一覧
              </v-subheader>
              <v-list-item
                link
                @click="topicCreateDialog = true"
              >
                <v-list-item-title>新しいトピックを作成する</v-list-item-title>
                <v-btn icon>
                  <v-icon color="grey lighten-1">
                    mdi-message-plus
                  </v-icon>
                </v-btn>
              </v-list-item>
              <v-list-item
                v-for="item in topicList"
                :key="item.comment_id"
                link
                @click="setDisplayMessageList(item)"
              >
                <v-list-item-content>
                  <v-list-item-title>{{ item.body }}</v-list-item-title>
                  <v-list-item-subtitle>{{ item.register_user_name }}</v-list-item-subtitle>
                </v-list-item-content>
                <v-btn icon>
                  <v-icon color="grey lighten-1">
                    mdi-message
                  </v-icon>
                </v-btn>
              </v-list-item>
            </v-list>
            <v-subheader>コメント</v-subheader>
            <v-divider />
            <div class="mt-2">
              <template v-for="(item, index) in rootMessageList">
                <v-divider
                  v-if="index != 0"
                  :key="`divider-${item.comment_id}`"
                />
                <div
                  :key="`div-${item.comment_id}`"
                  class="c-block-work-detail-comment"
                >
                  <v-avatar>
                    <v-img :src="item.avatar" />
                  </v-avatar>
                  <v-list-item-content>
                    <p>{{ item.body }}</p>
                  </v-list-item-content>
                </div>
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
                  Post
                </v-btn>
              </div>
            </div>
          </v-container>
        </v-card-text>
        <v-dialog
          v-model="topicDialog"
          scrollable
          fullscreen
          hide-overlay
          transition="dialog-bottom-transition"
        >
          <v-card class="pa-0">
            <v-card-title>
              <div class="c-block-work-detail-comment-topic">
                <v-avatar>
                  <v-img :src="selectedTopic.register_user_id" />
                </v-avatar>
                <p>{{ selectedTopic.body }}</p>
              </div>
            </v-card-title>
            <v-divider />
            <v-card-text>
              <v-subheader>コメント</v-subheader>
              <template v-for="item in topicMessageList">
                <div :key="item.comment_id">
                  <v-divider />
                  <div class="c-block-work-detail-comment">
                    <v-avatar>
                      <v-img :src="item.register_user_id" />
                    </v-avatar>
                    <v-list-item-content>
                      <p>{{ item.body }}</p>
                    </v-list-item-content>
                  </div>
                </div>
              </template>
              <v-textarea
                v-model="topicCommentBody"
                label="Leave a comment..."
                solo
              />
              <div style="display: flex;">
                <v-spacer />
                <v-btn
                  class="mx-0"
                  depressed
                  @click="postTopicCommentBody"
                >
                  Post
                </v-btn>
              </div>
            </v-card-text>
            <v-card-actions>
              <v-spacer />
              <v-btn
                color="primary"
                text
                @click="topicDialog = false"
              >
                閉じる
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
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
          <div style="display: flex;">
            <v-spacer />
            <v-btn
              class="mx-0"
              depressed
              @click="postTopic"
            >
              Post
            </v-btn>
          </div>
        </v-card-text>
        <v-card-actions>
          <v-spacer />
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
    },
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
      required: true, 
    }
  },
  data() {
    return {
      workDetail: {title: ""},
      question: null,
      imageList: [],
      rootMessageList: [],
      topicList: [],
      selectedTopic: {body: '', register_user_name: ''},
      topicMessageList: [],
      topicMessageDict: {},
      topicDialog: false,
      topicCreateDialog: false,
      rootCommentBody: '',
      topicCommentBody: '',
      topicBody: '',
    }
  },
  watch: {
    work() {
      this.findClassroomWork();
      this.getWorkCommentList();
    },
  },
  methods: {
    closeDialog() {
      this.$emit('closeDialog');
    },
    getLatest() {
      this.findClassroomWork();
      this.getWorkCommentList();
    },
    setDisplayMessageList(comment) {
      this.selectedTopic = comment;
      const l = this.topicMessageDict[comment.comment_id];
      if (l != undefined) {
        this.topicMessageList = l
	  } else {
        this.topicMessageList = []
      }
      this.topicDialog = true;
    },
    findClassroomWork() {
      if (this.work == null) return;
      if (this.classroom == null) return;
      const params = {"classroomId": this.classroom.classroom_id,  "workId": this.work.work_id}
      this.$store.dispatch("classroom/fetchClassroomWork", params)
        .then((data) => {
          this.workDetail = data['work']
          this.question = data['question']
          this.commentList = data['comment_list']
        })
        .catch((err) => {
          console.log(err);
        });
    },
    getWorkCommentList() {
      return new Promise((resolve, reject) => {
        if (this.work == null) return;
        if (this.classroom == null) return;
        const params = {"classroomId": this.classroom.classroom_id,  "workId": this.work.work_id}
        this.$store.dispatch("classroom/getWorkCommentList", params)
          .then((data) => {
            this.topicList = data['topic_list'];
            this.rootMessageList = data['root_message_list'];
            this.topicMessageDict = data['topic_message_dict']
            resolve(data);
          })
          .catch((err) => {
            console.log(err);
            reject(err);
          });
      });
    },
    postWorkComment(commentType, parentCommentId, body) {
      return new Promise((resolve, reject) => {
        if (this.work == null) return;
        if (this.classroom == null) return;
        const params = {classroomId: this.classroom.classroom_id,  workId: this.work.work_id, commentType, parentCommentId, body}
        this.$store.dispatch("classroom/postWorkComment", params)
          .then((data) => {
            this.getWorkCommentList()
              .then((data) => {
                resolve(data);
              })
              .catch((err) => {
                reject(err);
              });
          })
          .catch((err) => {
            alert('コメントの登録に失敗しました');
            reject(err);
          });
      });
    },
    postRootCommentBody() {
      this.postWorkComment('message', null, this.rootCommentBody)
        .then((data) => {
          this.rootCommentBody = '';
        });
    },
    postTopicCommentBody() {
	  this.postWorkComment('message', this.selectedTopic.comment_id, this.topicCommentBody)
        .then((data) => {
          const topicMessage = this.topicMessageDict[this.selectedTopic.comment_id];
          console.log('test')
          console.log(topicMessage)
          if (topicMessage instanceof Array) {
            console.log(this.topicMessageList)
            this.topicMessageList.splice(0, this.topicMessageList.length, ...topicMessage);
		  } else {
            this.topicMessageList.splice(0, this.topicMessageList.length, [data]);
		  }
          this.topicCommentBody = '';
        });
    },
    postTopic() {
	  this.postWorkComment('topic', null, this.topicBody)
        .then((data) => {
          this.topicBody = '';
          this.topicCreateDialog = false;
        });
    },
    getImageUrl(obj) {
      if (obj["image_url"] == null) { return false }
      const path = obj["image_url"];
      if (this.imageList[path] != null) { return true }
      this.$store.dispatch("getS3PublicFile", path)
        .then((url) => {
          this.$set(this.imageList, path, url);
        })
        .catch(() => {
          return false;
        });
      return true;
    },
  },
};
</script>

<style lang="scss" scoped>
.c-block-work-detail-comment-topic {
  padding: 8px;
  display: flex;
  align-items: flex-start;
  font-size: 15px;
  line-height: 1.5;
  p {
    padding: 0;
    margin-bottom: 0;
    text-align: left;
  }
  .v-list-item__content {
    margin-bottom: auto;
  }
}
.c-block-work-detail-comment {
  padding: 10px;
  display: flex;
  align-items: flex-start;
  p {
    padding: 0;
    text-align: left;
    margin-bottom: 0;
  }
  .v-list-item__content {
    margin-bottom: auto;
  }
}

.v-avatar {
  margin-right: 12px;
  background-color: #ededed;
}
</style>
