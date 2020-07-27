<template>
  <div>
    <v-card>
      <v-toolbar
        color="yellow darken-1"
        style="max-height: 56px;"
      >
        <v-btn
          icon
          @click="closeQuestionModifyDialog()"
        >
          <v-icon>mdi-close</v-icon>
        </v-btn>
        <v-toolbar-title>Toi(トイ)</v-toolbar-title>
        <v-spacer />
        <v-btn
          outlined
          text
          class="pa-2"
        >
          変更を保存する
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
                  v-model="questionForm.subjectName"
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
                  v-model="questionForm.sortTagList"
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
                    id="question-modify-editor-min"
                    v-model="questionForm.contents"
                    :editor-toolbar="customToolbarMin"
                    class="question-sentence-editor"
                    align="left"
                    use-custom-image-handler
                    @image-added="handleImageAdded"
                  />
                </div>
                <div class="custom-toolbar-max">
                  <vue-editor
                    id="question-modify-editor-max"
                    v-model="questionForm.contents"
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
  </div>
</template>

<script>
import schoolApiQuesionTransfer from "@/api/transfer/question.js";
import { VueEditor } from "vue2-editor";

export default {
  name: "QuestionModify",
  components: {
    VueEditor,
  },
  props: {
    selectedQuestion: {
      type: Object,
      required: true,
    },
    selectedContents: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      subjectList: schoolApiQuesionTransfer.getSubjectNameList(),
      tagItems: [],
      subjectNameRules: [(v) => !!v || "教科を選択してください"],
      questionForm: {
        subjectName: "",
        questionType: "describing",
        contents: "",
        sortTagList: [],
      },
      select: [],
      valid: true,
      customToolbarMax: [],
      customToolbarMin: [
        ["bold", "italic", "underline"],
        [{ list: "ordered" }, { list: "bullet" }],
        ["image", "code-block"],
      ],
      customToolbarType: "max",
    };
  },
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
    },
  },
  mounted() {
    this.customToolbarType = "min";
    this.questionForm = this.toFormData(
      this.selectedQuestion,
      this.selectedContents
    );
  },
  methods: {
    toFormData(question, contents) {
      console.log("整形");
      return {
        subjectName: question.subject_name,
        questionType: question.question_type,
        contents: contents,
        sortTagList: question.sort_tag_list,
      };
    },
    closeQuestionModifyDialog() {
      this.$emit("closeQuestionModifyDialog");
    },
    modifyQuestion() {
      this.$store
        .dispatch("question/modifyQuestion", {
          questionInput: this.questionForm,
        })
        .then(() => {
          alert("トイの編集に成功しました");
          this.$store.dispatch("question/fetchQuestionList");
          this.closeQuestionModifyDialog();
        });
    },
    handleImageAdded(file, Editor, cursorLocation, resetUploader) {
      console.log(cursorLocation);
      this.$store
        .dispatch("putS3PublicFile", {
          file: file,
        })
        .then((s3_key) => {
          this.$store
            .dispatch("getS3PublicFile", s3_key)
            .then((url) => {
              Editor.insertEmbed(cursorLocation, "image", url);
              resetUploader();
            })
            .catch((err) => {
              console.log(err);
            });
        })
        .catch((err) => {
          console.log(err);
        });
    },
    showMaxCustomToolbar() {
      this.customToolbarType = "max";
    },
    showMinCustomToolbar() {
      this.customToolbarType = "min";
    },
  },
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