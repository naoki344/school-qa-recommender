<template>
  <div>
    <v-dialog
      v-model="dialog"
      fullscreen
      persistent
      scrollable
      transition="dialog-bottom-transition"
    >
      <template v-slot:activator="{ on }">
        <v-btn
          style="width: 100%"
          text
          v-on="on"
        >
          <a style="text-align: right; display: block; width: 100%">新しいToi(トイ)を作成する</a>
        </v-btn>
      </template>
      <v-card>
        <v-toolbar
          color="yellow darken-1"
          style="max-height: 56px;"
        >
          <v-btn
            icon
            @click="dialog = false"
          >
            <v-icon>mdi-close</v-icon>
          </v-btn>
          <v-toolbar-title>Toi(トイ)</v-toolbar-title>
          <v-spacer />
          <v-btn
            text
            class="pa-2"
            @click="createQuestion"
          >
            作成する
          </v-btn>
        </v-toolbar>
        <v-card-text class="px-4">
          <v-container fluid>
            <v-form
              ref="form"
              v-model="valid"
              lazy-validation
            >
              <v-row align="center" class="toi-create-card-item-list">
                <v-col
                  class="pa-0"
                  cols="3"
                  md="2"
                  lg="1"
                >
                  <v-subheader class="pl-2">教科</v-subheader>
                </v-col>
                <v-col
                  class="pa-0"
                  cols="6"
                  md="2"
                  lg="2"
                >
                  <v-combobox
                    v-model="question.subjectName"
                    :items="subjectList"
                    label="好きな教科名を追加できます"
                    required
                    chips
                  />
                </v-col>
              </v-row>
              <v-row align="center">
                <v-col
                  class="pa-0"
                  cols="3"
                  md="2"
                  lg="1"
                >
                  <v-subheader class="pl-2">タグ</v-subheader>
                </v-col>
                <v-col
                  class="pa-0"
                  cols="9"
                  md="6"
                  lg="6"
                >
                  <v-combobox
                    v-model="question.sortTagList"
                    :items="tagItems"
                    label="好きなタグを追加できます"
                    class="toi-create-card-item-list"
                    multiple
                    required
                    chips
                  />
                </v-col>
              </v-row>
              <v-row>
                <v-col
                  class="pa-0 pt-4 mb-12"
                  cols="12"
                >
                  <div class="switch-custom-toolbar-text" v-if="customToolbarType === 'min'" @click="showMaxCustomToolbar"><a>ツールバーを全て表示</a></div>
                  <div class="switch-custom-toolbar-text" v-else @click="showMinCustomToolbar"><a>ツールバーを閉じる</a></div>
                  <div class="custom-toolbar-min">
                    <vue-editor
                      v-model="question.sentence.text"
                      :editor-toolbar="customToolbarMin"
                      class="question-sentence-editor"
                      align="left"
                    />
                  </div>
                  <div class="custom-toolbar-max">
                    <vue-editor
                      v-model="question.sentence.text"
                      class="question-sentence-editor"
                      :editor-toolbar="customToolbarMax"
                      align="left"
                    />
                  </div>
                </v-col>
              </v-row>
            </v-form>
          </v-container>
        </v-card-text>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import schoolApiQuesionTransfer from "@/api/transfer/question.js";
import { VueEditor } from "vue2-editor";

export default {
  name: "CreateQuestionDialog",
  components: {
    VueEditor
  },
  data: () => ({
    questionFormInit: {
      subjectName: "",
      questionType: "describing",
      estimatedTime: "",
      sentence: { text: "", imageUrl: "" },
      answer: { text: "", imageUrl: "" },
      commentary: { text: "", imageUrl: "" },
      sortTagList: [],
    },
    dialog: false,
    subjectList: schoolApiQuesionTransfer.getSubjectNameList(),
    sentenceImage: null,
    tagItems: ["初級"],
    timeList: [1, 3, 5, 15, 30, 60],
    subjectNameRules: [v => !!v || "教科を選択してください"],
    estimatedTimeRules: [v => !!v || "目安時間を選択してください"],
    question: {
      subjectName: "",
      questionType: "describing",
      estimatedTime: "",
      sentence: { text: "", imageUrl: null },
      answer: { text: "", imageUrl: null },
      commentary: { text: "", imageUrl: null },
      sortTagList: []
    },
    select: [],
    valid: true,
    customToolbarMax: [],
    customToolbarMin: [["bold", "italic", "underline"], [{ list: "ordered" }, { list: "bullet" }], ["image", "code-block"]],
    customToolbarType: "max",
  }),
  watch: {
    customToolbarType(value) {
      let maxInputDisplay = 'unset';
      let minInputDisplay = 'none';
      if (value === 'min') {
        maxInputDisplay = 'none';
        minInputDisplay = 'unset';
      }
      const minEle = document.getElementsByClassName("custom-toolbar-min")[0]
	  if (minEle !== undefined) {
        minEle.style.display = minInputDisplay;
      }
      const maxEle = document.getElementsByClassName("custom-toolbar-max")[0]
	  if (maxEle !== undefined) {
        maxEle.style.display = maxInputDisplay;
      }
    }
  },
  mounted() {
    this.customToolbarType = "min"
  },
  methods: {
    createQuestion() {
      const uploadQuestionImage = () => {
        return new Promise((resolve, reject) => {
          if (this.$refs.form.validate()) {
            this.snackbar = true;
          } else {
            this.valid = false;
            reject();
          }
          if (this.sentenceImage != null) {
            this.$store
              .dispatch("putS3PublicFile", {
                file: this.sentenceImage
              })
              .then(data => {
                this.question.sentence.imageUrl = data.key;
              })
              .catch(err => {
                console.log(err);
                reject();
              });
          } else {
            resolve();
          }
        });
      };
      const main = async () => {
        await uploadQuestionImage()
          .then(() => {
            this.$store
              .dispatch("question/createQuestion", {
                questionInput: this.question
              })
              .then(() => {
                this.$store.dispatch("question/fetchQuestionList");
                this.dialog = false;
              });
          })
          .catch(err => {
            console.log(err);
          });
      };
      main();
    },
    showMaxCustomToolbar() {
      this.customToolbarType = "max"
    },
    showMinCustomToolbar() {
      this.customToolbarType = "min"
    }
  }
};
</script>

<style lang="scss" scoped>
.switch-custom-toolbar-text {
  a {
    display: block;
    text-align: right;
  }
}

.custom-toolbar-min {
  display: unset;
}
.custom-toolbar-max {
  display: none;
}
.question-sentence-editor {
  height: 400px;
}

.toi-create-card-item-list {
  .v-list-item__content {
    flex: unset !important;
  }
}
</style>
