<template>
  <v-content>
    <v-item-group
      :mandatory="mandatory"
      :multiple="multiple"
    >
      <v-container>
        <v-row>
          <v-col
            cols="12"
            sm="6"
            md="6"
            lg="4"
            xl="3"
          >
            <create-question-dialog style="height: 100%; min-height: 200px; align-items: center;" />
          </v-col>
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
              v-if="type === 'cards'"
              class=""
              style="height: 100%; position:relative;"
              white
              @click="openQuestionDetailDialog(question)"
            >
              <v-img
                v-if="getImageUrl(question.question_sentence)"
                :src="imageList[question.question_sentence.image_url]"
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
                <div class="">
                  <h2>{{ question.subject_type | subjectTypeFilter }}</h2>
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
                  {{ question.question_sentence.text }}
                </div>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </v-item-group>
    <question-detail-dialog
      :question="selectedQuestion"
      :dialog-visible="questionDetailDialogVisible"
      @closeDialog="closeQuestionDetailDialog()"
    />
  </v-content>
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
    subjectTypeFilter: function(value) {
      if (!value) return "";
      return schoolApiQuesionTransfer.getSubjectNameFromType(value);
    },
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
    estimatedColorFilter: function(value) {
      if (!value) return "green";
      if (value <= 1) return "blue";
      if (value <= 5) return "green";
      if (value <= 15) return "orange";
      if (value > 15) return "red";
    },
  },
  data: () => ({
    types: ["cards", "images"],
    type: "cards",
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
      this.$store.dispatch("getS3PublicFile", path)
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
<style lang="scss">
div[name="amplify-s3-image"] > img {
  width: 100% !important;
  margin: unset;
  border-radius: unset !important;
  border: unset !important;
}
</style>
