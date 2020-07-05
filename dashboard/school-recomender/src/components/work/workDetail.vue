<!-- The ref attr used to find the swiper instance -->
<template>
  <v-container class="px-1">
    <v-card-text class="pa-1">
      <v-container class="pa-0">
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
                {{ work.title }}
              </v-card-title>
            </div>
            <div
              class="px-4 pb-4"
              style="display: flex; justify-content: flex-start;"
            >
              <v-chip
                small
                color="green"
                text-color="white"
              >
                {{ question.subject_name }}
              </v-chip>
              <v-chip
                v-for="tag in question.sort_tag_list"
                :key="tag"
                small
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
              <div
                id="work-detail-dialog-contents-text"
                style="word-break: break-all;"
              />
            </v-card-text>
            <v-divider />
            <v-row style="justify-content: space-around; ">
              <v-col
                cols="7"
                md="4"
                lg="4"
                class="py-2 pl-6"
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
                    <v-list-item
                      color="blue darken-2"
                      @click="topicCreateDialog = true"
                    >
                      <a style="font-family: HiraginoSans-W5;">トピックを作成</a>
                      <v-spacer />
                      <v-icon color="blue darken-2">
                        mdi-plus
                      </v-icon>
                    </v-list-item>
                  </template>
                </v-select>
              </v-col>
              <v-col
                cols="4"
                class="topic-creator px-0"
              >
                <div>
                  <v-avatar size="26">
                    <v-img
                      :src="
                        getUserAvatarImageUrl(
                          selectedTopic.register_user_id
                        )
                      "
                    />
                  </v-avatar>
                  <span class="font-weight-black ml-1">
                    {{
                      selectedTopic.register_user_name
                    }}
                  </span>
                </div>
              </v-col>

              <v-spacer />
            </v-row>
            <v-divider />

            <div
              v-for="item in topicMessageList"
              :key="item.comment_id"
              class="message px-3 py-2"
            >
              <v-hover v-slot:default="{ hover }">
                <div style="display:flex;">
                  <div
                    style="width: 100%;"
                    class="message-whole"
                  >
                    <v-avatar
                      tile
                      style="border-radius: 6px;"
                      size="44"
                    >
                      <v-img :src="getUserAvatarImageUrl(item.register_user_id)" />
                    </v-avatar>

                    <div
                      v-if="modifyingCommentId === item.comment_id"
                      class="message-area ms-3"
                    >
                      <textarea
                        :id="'textarea' + item.comment_id"
                        v-model="modifyingComment"
                        class="textarea"
                        @input="textAreaHeightSet(item.comment_id)"
                        @change="textAreaHeightSet(item.comment_id)"
                      />
                      <v-btn @click="cancelModifyingComment()">
                        キャンセル
                      </v-btn>
                      <v-btn color="yellow darken-1">
                        変更を保存する
                      </v-btn>
                    </div>

                    <div
                      v-else
                      class="message-area ms-3"
                    >
                      <p class="font-weight-bold ma-0 message-contributer-name">
                        {{ item.register_user_name }}
                        <span class="font-weight-medium message-time">
                          {{
                            item.register_date | messageTimeSortFilter
                          }}
                        </span>
                      </p>
                      <p class="font-weight-light mb-0 message-body">
                        {{ item.body }}
                      </p>
                    </div>
                  </div>
                  <div>
                    <v-btn
                      icon
                      :class="{'show-btn': hover}"
                      color="transparent"
                      @click="showModifyingComment(item.body,item.comment_id)"
                    >
                      <v-icon
                        small
                        :class="{'show-btn': hover}"
                        color="transparent"
                      >
                        mdi-pencil
                      </v-icon>
                    </v-btn>
                  </div>
                </div>
              </v-hover>
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
                autofocus
                @keydown.enter.shift.exact="postTopicCommentBody"
              />
              <v-btn
                :loading="loading"
                :disabled="loading"
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
            :loading="loading"
            :disabled="loading"
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
      width="400px"
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
            :loading="loading"
            :disabled="loading"
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
    <!-- コメントを編集するダイアログ -->
    <!-- ただし他人のコメントは編集できない -->
    <v-dialog v-model="commentModifyDialog">
      <v-card class="pa-0">
        <v-card-actions>
          <v-btn
            depressed
            icon
            @click="commentModifyDialog = false"
          >
            <v-icon>mdi-close</v-icon>
          </v-btn>
          <v-spacer />
          <v-btn
            :loading="loading"
            :disabled="loading"
            color="yellow darken-1"
            @click="postTopicCommentBody"
          >
            変更を保存する
          </v-btn>
        </v-card-actions>
        <v-divider />
        <v-card-text class="pa-1">
          <v-textarea
            v-model="modifyingComment"
            autofocus
            solo
            flat
            label="コメントを記入"
          />
        </v-card-text>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script>
import "swiper/dist/css/swiper.css";
import sanitizeHTML from "sanitize-html";
import moment from "moment";
export default {
  name: "WorkDetail",
  components: {},
  filters: {
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
  props: {
    workId: {
      type: Number,
      default: null
    },
    classroomId: {
      type: Number,
      default: null
    },
    question: {
      type: Object,
      default: null
    },
    work: {
      type: Object,
      default: null
    }
  },
  data() {
    return {
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
      commentModifyDialog: false,
      modifyingComment: "",
      modifyingCommentId: "",
      editingComment: "",
      editingCommentDict: {},
      loading: false
    };
  },
  computed: {
    topicSelectList() {
      console.log("computed始め" + msgList);
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
      console.log("computed終わり" + msgList);
      return msgList;
    }
  },
  created() {
    console.log("created始め" + this.topicSelectList);
    this.getWorkCommentList().then(this.setInitialTopic);
    console.log("created終わり" + this.topicSelectList);
  },
  mounted() {
    const contents = document.getElementById(
      "work-detail-dialog-contents-text"
    );
    contents.innerHTML = sanitizeHTML(
      this.question.question_sentence.contents,
      {
        allowedTags: [
          "h3",
          "h4",
          "h5",
          "h6",
          "blockquote",
          "p",
          "a",
          "ul",
          "ol",
          "nl",
          "li",
          "b",
          "i",
          "strong",
          "em",
          "strike",
          "abbr",
          "code",
          "hr",
          "br",
          "div",
          "table",
          "thead",
          "caption",
          "tbody",
          "tr",
          "th",
          "td",
          "pre",
          "iframe",
          "img"
        ],
        allowedAttributes: { img: ["s3-key"], a: ["href", "target"] }
      }
    );
    console.log(contents.innerHTML);
    const imgList = contents.getElementsByTagName("img");
    imgList.forEach(async img => {
      const url = await this.getImageUrl(
        "thumbnail/w512/" + img.getAttribute("s3-key")
      );
      img.setAttribute("src", url);
      img.style.width = "100%";
    });
    if (this.modifyingCommentId != "") {
      console.log("success");
      this.textAreaHeightSet(modifyingCommentId);
    }
  },
  methods: {
    textAreaHeightSet(Id) {
      console.log("dekita");
      let element = document.getElementById("textarea" + Id);
      // テキストエリアにフォーカスを当てる
      element.focus();
      // 一旦テキストエリアを小さくしてスクロールバー（縦の長さを取得）
      element.style.height = "10px";
      let wSclollHeight = parseInt(element.scrollHeight);
      // 1行の長さを取得する
      let wLineH = parseInt(element.style.lineHeight.replace(/px/, ""));
      // 最低2行の表示エリアにする
      if (wSclollHeight < wLineH * 2) {
        wSclollHeight = wLineH * 2;
      }
      // テキストエリアの高さを設定する
      element.style.height = wSclollHeight + "px";
    },
    cancelModifyingComment() {
      this.modifyingCommentId = "";
    },
    openCommentModifyArea(body, Id) {
      this.modifyingCommentId = Id;
      this.modifyingComment = body;
      if (this.modifyingCommentId != "") {
        this.$nextTick(() => {
          this.textAreaHeightSet(this.modifyingCommentId);
        });
      }
    },
    openCommentModifyDialog(body) {
      this.commentModifyDialog = true;
      this.modifyingComment = body;
    },
    showModifyingComment(body, Id) {
      let windowWidth = window.innerWidth;
      const breakPoint = 760;
      let isMobileSize = windowWidth < breakPoint;
      let isPcSize = windowWidth >= breakPoint;
      if (isMobileSize) {
        this.openCommentModifyDialog(body);
      }
      if (isPcSize) {
        this.openCommentModifyArea(body, Id);
      }
    },
    setInitialTopic() {
      console.log("初期表示" + this.topicList);
      this.selectedTopic = this.topicList.find(item => item.body === "メイン");
      this.selectedTopicId = this.selectedTopic.comment_id;
      const l = this.topicMessageDict[this.selectedTopicId];
      if (l != undefined) {
        this.topicMessageList = l;
      } else {
        this.topicMessageList = [];
      }

      console.log("初期トピック表示");
    },

    goToBottom() {
      var element = document.documentElement;
      var different = element.scrollHeight - element.clientHeight;
      window.scroll(0, different);
    },
    getLatest() {
      this.getWorkCommentList();
    },
    setDisplayMessageList(newCommentId) {
      console.log("メッセセット開始");
      // 編集中のコメントを保存
      const beforeCommentId = this.selectedTopic.comment_id;
      if (beforeCommentId !== undefined) {
        this.editingCommentDict[beforeCommentId] = this.editingComment;
      }
      // 選択したトピックのコメントをテキストエリアに表示
      const editingComment = this.editingCommentDict[newCommentId];
      if (editingComment !== undefined) {
        this.editingComment = editingComment;
      } else {
        this.editingComment = "";
      }

      this.selectedTopic = this.topicList.find(
        item => item.comment_id === newCommentId
      );
      const l = this.topicMessageDict[newCommentId];
      if (l != undefined) {
        this.topicMessageList = l;
      } else {
        this.topicMessageList = [];
      }
      console.log("メッセセット完了");
    },
    getWorkCommentList() {
      console.log("getWorkCommentList始め");
      return new Promise((resolve, reject) => {
        if (this.workId == null) return;
        if (this.classroomId == null) return;
        const params = {
          classroomId: this.classroomId,
          workId: this.workId
        };
        this.$store
          .dispatch("classroom/getWorkCommentList", params)
          .then(data => {
            this.topicList = data["topic_list"];
            this.rootMessageList = data["root_message_list"];
            this.topicMessageDict = data["topic_message_dict"];
            resolve(data);
            console.log("getWorkCommentList完了");
          })
          .catch(err => {
            console.log(err);
            reject(err);
          });
      });
    },
    postWorkComment(commentType, parentCommentId, body) {
      return new Promise((resolve, reject) => {
        if (this.workId == null) return;
        if (this.classroomId == null) return;
        const params = {
          classroomId: this.classroomId,
          workId: this.workId,
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
      this.loading = true;
      this.goToBottom();
      this.postWorkComment(
        "message",
        this.selectedTopic.comment_id,
        this.editingComment
      ).then(data => {
        const topicMessage = this.topicMessageDict[
          this.selectedTopic.comment_id
        ];
        if (topicMessage instanceof Array) {
          this.topicMessageList.splice(
            0,
            this.topicMessageList.length,
            ...topicMessage
          );
        } else {
          this.topicMessageList.splice(0, this.topicMessageList.length, [data]);
        }
        this.loading = false;
        this.editingComment = "";
        this.postCommentDialog = false;
      });
    },
    postTopic() {
      if (!(this.topicBody && this.topicBody.match(/\S/g))) return;
      this.loading = true;
      this.postWorkComment("topic", null, this.topicBody).then(data => {
        this.topicBody = "";
        this.topicCreateDialog = false;
        this.selectedTopicId = this.topicSelectList.slice(-1)[0];
        this.setDisplayMessageList(this.selectedTopicId.value);
        this.loading = false;
      });
      // セレクトボックスでのトピック切り替えをシミュレーション
    },
    async getImageUrl(s3Key) {
      if (s3Key == null) {
        return null;
      }
      if (this.imageList[s3Key] != null) {
        return this.imageList[s3Key];
      }
      const url = await this.$store
        .dispatch("getS3PublicFile", s3Key)
        .then(async url => {
          await this.$set(this.imageList, s3Key, url);
          return this.imageList[s3Key];
        })
        .catch(() => {
          return null;
        });
      return url;
    }
  }
};
</script>

<style lang="scss" scoped>
.message {
  word-break: break-all;
}
.message:hover {
  background-color: #ededed;
}
.message-whole {
  display: flex;
  max-width: 100%;
}
.message-area {
  display: inline-block;
  width: 100%;
  .textarea {
    width: 100%;
    height: 10vh;
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
.show-btn {
  color: rgba(0, 0, 0, 1) !important;
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
  word-break: break-all;
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

// pc/タブレットの時
@media screen and (min-width: 760px) {
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
