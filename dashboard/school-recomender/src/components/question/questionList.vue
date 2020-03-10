<template>
  <v-container>
    <v-item-group :mandatory="mandatory" :multiple="multiple">
      <v-container class="pa-0">
        <v-row>
          <v-col cols="12" sm="12" md="6" lg="4" xl="3">
            <create-question-dialog style="height: 100%;"></create-question-dialog>
          </v-col>
          <v-col
            v-for="question in questionCardList"
            :key="question.question_id"
            cols="12"
            sm="12"
            md="6"
            lg="4"
            xl="3"
          >
            <v-item v-slot:default="{ active, toggle }">
              <v-card
                v-if="type === 'cards'"
                :color="active ? 'grey darken' : ''"
                class=""
                style="height: 100%;"
                white
                @click="toggle"
              >
                <v-card-text>
                  <div class="mb-2" style="display: flex; justify-content: space-between">
                    <div>{{question.register_date | dateTimeFilter}} ({{question.register_user_name}})</div>
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
                      >{{question.estimated_time}}</v-avatar>Min
                    </v-chip>
                  </div>
                  <div class="d-flex">
                    <v-col cols="4">
                      <!--amplify-s3-image name="amplify-s3-image" v-if="exists(question.question_sentence, 'image_url')" :imagePath="question.question_sentence.image_url" style="width: 100%"/-->
                      <img v-if="getImageUrl(question.question_sentence)" :src="imageList[question.question_sentence.image_url]" style="width: 100%"/>
                    </v-col>
                    <v-col cols="8">
                      <h2
                        class=""
                      >【{{question.subject_type | subjectTypeFilter}}】{{question.sort_tag_list | sortTagListFilter}}</h2>
                    </v-col>
                  </div>
                  <p>{{question.question_type | questionTypeFilter}}</p>
                  <div class="text--primary">{{question.question_sentence.text}}</div>
                </v-card-text>
                <v-scroll-y-transition>
                  <div
                    v-if="active"
                    class="display-1 font-weight-bold"
                    style="position: absolute; right:5px; bottom:0;"
                  >Add</div>
                </v-scroll-y-transition>
              </v-card>
            </v-item>
          </v-col>
        </v-row>
      </v-container>
    </v-item-group>
  </v-container>
</template>

<script>
import { mapState } from "vuex";
import moment from "moment";
import "@mdi/font/css/materialdesignicons.css";
import createQuestionDialog from "@/components/question/createQuestionDialog.vue";
import schoolApiQuesionTransfer from "@/api/transfer/question.js";

export default {
  name: "QuestionIndex",
  components: {
    createQuestionDialog
  },
  data: () => ({
    types: ["cards", "images"],
    type: "cards",
    username: "",
    password: "",
    showPassword: false,
    mandatory: false,
    multiple: true,
    dialog: false,
    questionList: [],
    url: "",
    imageList: [],
  }),
  computed: {
    ...mapState({
      questionCardList: state => state.question.questionCardList
    })
  },
  methods: {
    fetchQuestionList() {
      this.$store.dispatch("question/fetchQuestionList");
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
  created() {
    this.fetchQuestionList();
    document.getElementById("dv1");
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
    sortTagListFilter: function(value) {
      if (!value) return "";
      return value.join(",");
    },
    estimatedColorFilter: function(value) {
      if (!value) return "green";
      if (value <= 1) return "blue";
      if (value <= 5) return "green";
      if (value <= 15) return "orange";
      if (value > 15) return "red";
    },
  }
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
