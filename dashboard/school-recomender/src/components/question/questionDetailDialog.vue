<template>
  <v-content>
    <v-row justify="center">
      <v-dialog v-model="dialogVisible" max-width="600" @click:outside="closeDialog()" @keydown.esc="closeDialog()">
        <v-card>
          <div class="px-4 pt-3 pb-2" style="display: flex; justify-content: space-between">
            <v-card-title class="headline font-weight-bold" style="padding: 0;">{{question.subject_type | subjectTypeFilter}}</v-card-title>
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
          <div class="px-4 pb-4" style="display: flex; justify-content: letf">
            <v-chip v-for="tag in question.sort_tag_list" :key="tag" style="margin-right:5px;">{{tag}}</v-chip>
          </div>
          <v-divider class="pb-4"/>
          <v-card-text class="pb-2 px-4 title" style="text-align: left;">＜問い＞</v-card-text>
          <v-img class="mb-2" v-if="getImageUrl(question.question_sentence)" :src="imageList[question.question_sentence.image_url]" style="width: 100%;"/>
          <v-card-text class="px-4 pt-0 pb-6 body-1" style="text-align: left;">{{question.question_sentence.text}}</v-card-text>

          <v-card-text class="pb-2 px-4 title" style="text-align: left;">＜解答＞</v-card-text>
          <v-img class="pb-2" v-if="getImageUrl(question.question_answer)" :src="imageList[question.question_answer.image_url]" style="width: 100%;"/>
          <v-card-text class="px-4 pt-0 pb-6 body-1" style="text-align: left;">{{question.question_answer.text}}</v-card-text>

          <v-card-text class="pb-2 px-4 title" style="text-align: left;">＜解説＞</v-card-text>
          <v-img class="pb-2" v-if="getImageUrl(question.question_answer)" :src="imageList[question.question_answer.image_url]" style="width: 100%;"/>
          <v-card-text class="px-4 pt-0 pb-6 body-1" style="text-align: left;">{{question.question_answer.text}}</v-card-text>
          <v-divider class="pb-4"/>
          <v-card-text class="pb-2 px-4 title" style="text-align: left;">クラス一覧</v-card-text>
          <v-container fluid class="px-4 py-0">
            <v-checkbox v-for="room in classroomList" :key="room.classroom.classroom_id" class="pa-0" v-model="selectedClassroom" :label="room.classroom.name" :value="room.classroom.classroom_id" />
          </v-container>
          <v-form>
            <div v-if="selectedClassroom.length > 0" class="pb-2 px-4">
              <v-text-field v-model="workTitle" counter="25" label="ワークのタイトル" required></v-text-field>
              <v-text-field v-model="workCaption" counter="25" label="ワークの説明" required></v-text-field>
              <v-btn style="height: 100%" col=12 class="ma-2 py-2 px-4" tile outlined color="success" @click="registerWorkSelectedClassroom()">選択した{{selectedClassroom.length}}つのクラスに<br />この問いを投稿</v-btn>
            </div>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="green darken-1" text @click="closeDialog()"
                >閉じる</v-btn
              >
            </v-card-actions>
          </v-form>
        </v-card>
      </v-dialog>
    </v-row>
  </v-content>
</template>

<script>
import { mapState } from "vuex";
import schoolApiQuesionTransfer from "@/api/transfer/question.js";
import moment from "moment";

export default {
  name: "questionDetailDialog",
  props: {
    dialogVisible: {
      type: Boolean
    },
    question: {
      type: Object
    }
  },
  data: () => ({
    imageList: [],
    selectedClassroom: [],
    workCaption: '',
    workTitle: '',
  }),
  computed: {
    ...mapState({
      classroomList: state => state.classroom.myClassroomList
    })
  },
  methods: {
    closeDialog() {
      this.selectedClassroom = [];
      this.$emit('closeDialog');
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
    fetchClassroomList() {
      this.$store.dispatch("classroom/fetchMyClassroomList");
      console.log(this.classroomList[0]);
    },
    registerWorkSelectedClassroom() {
      this.$store.dispatch("classroom/registerWork",
        {question: this.question, selectedClassroom: this.selectedClassroom,
		title: this.workTitle, caption: this.workCaption})
        .then(() => {
          alert("クラスへの投稿に成功しました。");
          this.closeDialog();
        });
    }
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
  mounted() {
    this.fetchClassroomList();
  }
};
</script>

