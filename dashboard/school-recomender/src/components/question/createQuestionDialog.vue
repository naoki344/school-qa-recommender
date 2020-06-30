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
              <v-row
                align="center"
                class="toi-create-card-item-list"
              >
                <v-col
                  class="pa-0"
                  cols="3"
                  md="2"
                  lg="1"
                >
                  <v-subheader class="pl-2">
                    教科
                  </v-subheader>
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
                  <v-subheader class="pl-2">
                    タグ
                  </v-subheader>
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
                  <div
                    v-if="customToolbarType === 'min'"
                    class="switch-custom-toolbar-text"
                    @click="showMaxCustomToolbar"
                  >
                    <a>ツールバーを全て表示</a>
                  </div>
                  <div
                    v-else
                    class="switch-custom-toolbar-text"
                    @click="showMinCustomToolbar"
                  >
                    <a>ツールバーを閉じる</a>
                  </div>
                  <div class="custom-toolbar-min">
                    <vue-editor
                      id="editor-min"
                      v-model="question.contents"
                      :editor-toolbar="customToolbarMin"
                      class="question-sentence-editor"
                      align="left"
                      use-custom-image-handler
                      @image-added="handleImageAdded"
                    />
                  </div>
                  <div class="custom-toolbar-max">
                    <vue-editor
                      id="editor-max"
                      v-model="question.contents"
                      class="question-sentence-editor"
                      :editor-toolbar="customToolbarMax"
                      align="left"
                      use-custom-image-handler
                      @image-added="handleImageAdded"
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
const questionInit = {
  subjectName: "",
  questionType: "describing",
  contents: "",
  sortTagList: []
};

export default {
  name: "CreateQuestionDialog",
  components: {
    VueEditor
  },
  data: () => ({
    dialog: false,
    subjectList: schoolApiQuesionTransfer.getSubjectNameList(),
    tagItems: [],
    timeList: [1, 3, 5, 15, 30, 60],
    subjectNameRules: [v => !!v || "教科を選択してください"],
    question: JSON.parse(JSON.stringify(questionInit)),
    select: [],
    valid: true,
    customToolbarMax: [],
    customToolbarMin: [
      ["bold", "italic", "underline"],
      [{ list: "ordered" }, { list: "bullet" }],
      ["image", "code-block"]
    ],
    customToolbarType: "max"
  }),
  watch: {
    customToolbarType(value) {
      let maxInputDisplay = "unset";
      let minInputDisplay = "none";
      if (value === "min") {
        maxInputDisplay = "none";
        minInputDisplay = "unset";
      }
      const minEle = document.getElementsByClassName("custom-toolbar-min")[0];
      if (minEle !== undefined) {
        minEle.style.display = minInputDisplay;
      }
      const maxEle = document.getElementsByClassName("custom-toolbar-max")[0];
      if (maxEle !== undefined) {
        maxEle.style.display = maxInputDisplay;
      }
    }
  },
  mounted() {
    this.customToolbarType = "min";
  },
  methods: {
    async createQuestion() {
      this.$store
        .dispatch("question/createQuestion", {
          questionInput: this.question
        })
        .then(() => {
          this.question = JSON.parse(JSON.stringify(questionInit));
          this.$store.dispatch("question/fetchQuestionList");
          this.dialog = false;
        });
    },
    handleImageAdded(file, Editor, cursorLocation, resetUploader) {
      console.log(cursorLocation);
      this.$store
        .dispatch("putS3PublicFile", {
          file: file
        })
        .then(s3_key => {
          this.$store
            .dispatch("getS3PublicFile", s3_key)
            .then(url => {
              Editor.insertEmbed(cursorLocation, "image", url);
              resetUploader();
            })
            .catch(err => {
              console.log(err);
            });
        })
        .catch(err => {
          console.log(err);
        });
    },
    showMaxCustomToolbar() {
      this.customToolbarType = "max";
    },
    showMinCustomToolbar() {
      this.customToolbarType = "min";
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
