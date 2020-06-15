<template>
  <div>
    <v-item-group
      :mandatory="mandatory"
      :multiple="multiple"
    >
      <v-container>
        <create-question-dialog />
        <v-divider class="mb-4" />
        <v-row
          v-if="questionCardList.length > 0"
        >
          <v-col
            v-for="question in questionCardList"
            :key="question.question_id"
            cols="12"
            sm="6"
            md="6"
            lg="4"
            xl="3"
          >
            <v-card
              style="height: 100%; position:relative;"
              white
              @click="openQuestionDetailDialog(question)"
            >
              <v-img
                v-if="getImageUrl(question)"
                :src="imageList[question.image_url]"
                style="width: 100%; height: 200px;"
              />
              <v-img
                v-else
                src="@/assets/question-no-image.png"
                style="width: 100%; height: 200px;"
              />
              <v-card-text class="mb-2">
                <div
                  class="mb-2"
                  style="display: flex; justify-content: space-between"
                >
                  <div>{{ question.register_date | dateTimeFilter }} ({{ question.register_user_name }})</div>
                  <v-chip
                    class
                    small
                    color="green"
                    text-color="white"
                  >
                    {{ question.subject_name }}
                  </v-chip>
                </div>
                <div class="">
                  <p style="margin: 0;">
                    {{ question.question_type | questionTypeFilter }}
                  </p>
                </div>
                <v-chip
                  v-for="tag in question.sort_tag_list"
                  :key="tag"
                  style="margin:0 5px;"
                >
                  {{ tag }}
                </v-chip>
                <div class="text--primary">
                  {{ question.question_sentence.summary }}
                </div>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
        <v-row
          v-else
          class="mb-4"
        >
          <h5 class="question-no-text">
            トイが作成されていません。
          </h5>
        </v-row>
      </v-container>
    </v-item-group>
    <question-detail-dialog
      v-if="questionDetailDialogVisible"
      :question="selectedQuestion"
      :dialog-visible="questionDetailDialogVisible"
      @closeDialog="closeQuestionDetailDialog()"
    />
  </div>
</template>

<script>
import { mapState } from "vuex";
import moment from "moment";
import "@mdi/font/css/materialdesignicons.css";
import createQuestionDialog from "@/components/question/createQuestionDialog.vue";
import questionDetailDialog from "@/components/question/questionDetailDialog.vue";
import schoolApiQuesionTransfer from "@/api/transfer/question.js";

export default {
  name: "QuestionIndex",
  components: {
    createQuestionDialog,
    questionDetailDialog
  },
  filters: {
    questionTypeFilter: function(value) {
      if (!value) return "";
      if (value === "describing") return "記述式";
      if (value === "selectable") return "選択式";
      return "";
    },
    dateTimeFilter: function(value) {
      if (!value) return "";
      return moment(value).format("MM月DD日 hh:mm");
    },
  },
  data: () => ({
    username: "",
    password: "",
    showPassword: false,
    mandatory: false,
    multiple: true,
    questionList: [],
    url: "",
    imageList: [],
    selectedQuestion: schoolApiQuesionTransfer.getQuestionModel(),
    questionDetailDialogVisible: false,
  }),
  computed: {
    ...mapState({
      questionCardList: state => state.question.questionCardList
    })
  },
  created() {
    this.fetchQuestionList();
  },
  methods: {
    fetchQuestionList() {
      this.$store.dispatch("question/fetchQuestionList");
    },
    openQuestionDetailDialog(question) {
      this.$store.dispatch("question/fetchQuestion", question.question_id)
        .then((question) => {
          this.selectedQuestion = question;
          this.questionDetailDialogVisible = true;
        });
    },
    closeQuestionDetailDialog() {
      this.selectedQuestion = schoolApiQuesionTransfer.getQuestionModel()
      this.questionDetailDialogVisible = false;
    },
    getImageUrl(obj) {
      if (obj["image_url"] == null) { return false }
      const path = obj["image_url"];
      if (this.imageList[path] != null) { return true }
      const thumbPath = "thumbnail/w512/" + path;
      this.$store.dispatch("getS3PublicFile", thumbPath)
        .then((url) => {
          this.$set(this.imageList, path, url);
        })
        .catch(() => {
          return false;
        });
      return true;
    },
    imageUrlFilter(value){
      return value;
    }
  },
};
</script>
<style lang="scss" scoped>
div[name="amplify-s3-image"] > img {
  width: 100% !important;
  margin: unset;
  border-radius: unset !important;
  border: unset !important;
}

.question-no-text {
  margin-top: 40px;
  display: block;
  text-align: center;
  width: 100%;
}
</style>
