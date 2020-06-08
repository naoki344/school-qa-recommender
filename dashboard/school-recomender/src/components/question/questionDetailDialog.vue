<template>
  <v-content id="question-detail-dialog">
    <v-row justify="center">
      <v-dialog
        v-model="dialogVisible"
        max-width="600"
        @click:outside="closeDialog()"
        @keydown.esc="closeDialog()"
      >
        <v-card>
          <v-card-title
            class="pb-2 px-4 title"
            style="text-align: center;"
          >
            Toi
          </v-card-title>
          <div
            class="px-4 pt-3 pb-2"
            style="display: flex; justify-content: space-between"
          >
            <v-chip
              class
              :color="question.estimated_time | estimatedColorFilter"
              text-color="white"
            >
              {{ question.subject_name }}
            </v-chip>
            <div
              class="px-4 pb-4"
              style="display: flex;"
            >
              <v-chip
                v-for="tag in question.sort_tag_list"
                :key="tag"
                style="margin-right:5px;"
              >
                {{ tag }}
              </v-chip>
            </div>
          </div>
          <v-card-text
            id="question-detail-dialog-contents"
            class="px-4 pt-0 pb-6 body-1 question-sentence-contents"
            style="text-align: left;"
          >
            <div id="question-detail-dialog-contents-text" />
          </v-card-text>

          <v-divider class="pb-4" />
          <v-card-text
            class="pb-2 px-4 title"
            style="text-align: left;"
          >
            クラス一覧
          </v-card-text>
          <v-container
            fluid
            class="px-4 py-0"
          >
            <v-checkbox
              v-for="room in classroomList"
              :key="room.classroom.classroom_id"
              v-model="selectedClassroom"
              class="pa-0"
              :label="room.classroom.name"
              :value="room.classroom.classroom_id"
            />
          </v-container>
          <v-form
            v-model="inputFormIsValid"
          >
            <div
              v-if="selectedClassroom.length > 0"
              align="center"
              class="pb-2 px-4"
            >
              <v-text-field
                v-model="workTitle"
                counter="25"
                label="ワークのタイトル"
                :rules="[rules.required]"
              />
              <v-text-field
                v-model="workCaption"
                counter="25"
                label="ワークの説明"
                :rules="[rules.required]"
              />
              <v-btn
                style="height: 100%"
                col="12"
                class="ma-2 py-2 px-4"
                tile
                outlined
                color="success"
                :disabled="!inputFormIsValid"
                @click="registerWorkSelectedClassroom()"
              >
                選択した{{ selectedClassroom.length }}つのクラスに<br>この問いを投稿
              </v-btn>
            </div>
            <v-card-actions>
              <v-spacer />
              <v-btn
                color="green darken-1"
                text
                @click="closeDialog()"
              >
                閉じる
              </v-btn>
            </v-card-actions>
          </v-form>
        </v-card>
      </v-dialog>
    </v-row>
  </v-content>
</template>

<script>
import { mapState } from "vuex";
import moment from "moment";
import sanitizeHTML from 'sanitize-html'

export default {
  name: "QuestionDetailDialog",
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
    estimatedColorFilter: function(value) {
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
    question: {
      type: Object,
      required: true
    }
  },
  data: () => ({
    imageList: [],
    selectedClassroom: [],
    workCaption: '',
    workTitle: '',
    contents: '',
    rules: {
      required: value => !!value || "入力されていません",
    },
    inputFormIsValid: false,
  }),
  computed: {
    ...mapState({
      classroomList: state => state.classroom.myClassroomList
    })
  },
  mounted() {
    this.fetchClassroomList();
    const contents = document.getElementById('question-detail-dialog-contents-text');
    contents.innerHTML = sanitizeHTML(this.question.question_sentence.contents,
      {
        allowedTags: [ 'h3', 'h4', 'h5', 'h6', 'blockquote', 'p', 'a', 'ul', 'ol',
  'nl', 'li', 'b', 'i', 'strong', 'em', 'strike', 'abbr', 'code', 'hr', 'br', 'div',
  'table', 'thead', 'caption', 'tbody', 'tr', 'th', 'td', 'pre', 'iframe', 'img' ],
        allowedAttributes: {"img": ["s3-key"]}
      })
    console.log(contents.innerHTML);
    const imgList = contents.getElementsByTagName("img");
    imgList.forEach(async img => {
      const url = await this.getImageUrl(
        "thumbnail/w512/" + img.getAttribute("s3-key")
      );
      img.setAttribute("src", url);
      img.style.width = "100%";
    });
  },
  methods: {
    closeDialog() {
      this.selectedClassroom = [];
      this.$emit('closeDialog');
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
    fetchClassroomList() {
      this.$store.dispatch("classroom/fetchMyClassroomList");
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
};
</script>


<style lang="scss">
.question-sentence-contents {
  img {
    width: 100%;
  }
}
</style>
