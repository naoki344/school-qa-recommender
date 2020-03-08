<template>
  <v-item>
    <v-card class="d-flex align-center" height="200">
      <v-row justify="center">
        <v-dialog v-model="dialog" persistent width="98%">
          <template v-slot:activator="{ on }">
            <v-btn color="green" dark v-on="on">新しい問いを追加</v-btn>
          </template>
          <v-card>
            <v-card-title class="headline">新しい問いを作成する</v-card-title>
            <v-card-text
              >問題の形式をタブから選び、問いおよび回答を入力してください。</v-card-text
            >
            <v-tabs :vertical="false">
              <v-tab><v-icon left>mdi-grease-pencil</v-icon>記述式</v-tab>
              <v-tab-item>
                <v-card flat>
                  <v-card-text>
                    <v-container fluid>
                      <v-form ref="form" v-model="valid" lazy-validation>
                        <v-row align="center">
                          <v-col cols="4" md="2" lg="2">
                            <v-subheader>教科</v-subheader>
                          </v-col>
                          <v-col cols="8" md="2" lg="2">
                            <v-select
                              v-model="question.subjectName"
                              :rules="subjectNameRules"
                              :items="subjectList"
                              menu-props="auto"
                              label="Select"
                              single-line
                              required
                            ></v-select>
                          </v-col>
                          <v-col cols="4" md="2" lg="2">
                            <v-subheader>回答時間</v-subheader>
                          </v-col>
                          <v-col cols="8" md="2" lg="2">
                            <v-select
                              v-model="question.estimatedTime"
                              :rules="estimatedTimeRules"
                              :items="timeList"
                              menu-props="auto"
                              label="Select"
                              single-line
                              required
                            ></v-select>
                          </v-col>
                        </v-row>
                        <v-row>
                          <v-col cols="4" md="2" lg="2">
                            <v-subheader>タグ</v-subheader>
                          </v-col>
                          <v-col cols="8" md="6" lg="6">
                            <v-combobox
                              v-model="question.sortTagList"
                              :items="tagItems"
                              label="自由作成可"
                              multiple
                              required
                              chips
                            ></v-combobox>
                          </v-col>
                        </v-row>
                        <v-row align="center">
                          <v-col cols="12" md="9" lg="9">
                            <v-textarea
                              v-model="question.sentence.text"
                              label="問い(画像は<image> のある場所に表示されます)"
                              required
                            ></v-textarea>
                          </v-col>
                          <v-col clos="12" md="3" lg="3">
                            <v-file-input
                              chips
                              label="問い添付画像"
                              accept="image/*"
                              show-size
                              @change="onSentenceImageChange"
                              v-model="sentenceImage" />
                          </v-col>
                        </v-row>
                        <v-row align="center">
                          <v-col cols="12" md="9" lg="9">
                            <v-textarea
                              v-model="question.answer.text"
                              label="模範回答(画像は<image> のある場所に表示されます)"
                              required
                            ></v-textarea>
                          </v-col>
                          <v-col clos="12" md="3" lg="3">
                            <v-file-input
                              chips
                              label="回答添付画像"
                              accept="image/*"
                              @change="onAnswerImageChange"
                              v-model="answerImage" />
                          </v-col>
                        </v-row>
                        <v-row align="center">
                          <v-col cols="10" md="9" lg="9">
                            <v-textarea
                              v-model="question.commentary.text"
                              label="解説(画像は<image> のある場所に表示されます)"
                              required
                            ></v-textarea>
                          </v-col>
                          <v-col clos="2" md="3" lg="3">
                            <v-file-input
                              chips
                              label="解説添付画像"
                              accept="image/*"
                              @change="onCommentaryImageChange"
                              v-model="commentaryImage" />
                          </v-col>
                        </v-row>
                      </v-form>
                    </v-container>
                  </v-card-text>
                </v-card>
              </v-tab-item>

              <v-tab><v-icon left>mdi-check-underline</v-icon>選択式</v-tab>
              <v-tab-item>
                <v-card flat>
                  <v-card-text>
                    <p></p>
                  </v-card-text>
                </v-card>
              </v-tab-item>
            </v-tabs>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="green darken-1" text @click="dialog = false"
                >閉じる</v-btn
              >
              <v-btn color="green darken-1" @click="createQuestion">作成する</v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
      </v-row>
    </v-card>
  </v-item>
</template>

<script>
import schoolApiQuesionTransfer from "@/api/transfer/question.js";
export default {
  name: "CreateQuestionDialog",
  data: () => ({
    questionFormInit: {
      subjectName: "",
      questionType: "describing",
      estimatedTime: "",
      sentence: { text: "", imageUrl: '' },
      answer: { text: "", imageUrl: '' },
      commentary: { text: "", imageUrl: '' },
      sortTagList: []
    },
    dialog: false,
    subjectList: schoolApiQuesionTransfer.getSubjectNameList(),
    sentenceImage: null,
    answerImage: null,
    commentaryImage: null,
    tagItems: ["因数分解", "初級"],
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
    valid: true
  }),
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
            this.$store.dispatch("putS3PublicFile", {
              file: this.sentenceImage,
              })
              .then((data) => {
                this.question.sentence.imageUrl = data.key;
                if (this.answerImage != null) {
                  this.$store.dispatch("putS3PublicFile", {
                    file: this.answerImage,
                    })
                    .then((data) => {
                      this.question.answer.imageUrl = data.key;
                      if (this.commentaryImage != null) {
                        this.$store.dispatch("putS3PublicFile", {
                          file: this.commentaryImage,
                          })
                          .then((data) => {
                            this.question.commentary.imageUrl = data.key;
                            resolve();
                          })
                          .catch(err => {
                            console.log(err);
                            reject();
                          });
                      } else {
                        resolve();
                      }
                    })
                    .catch(err => {
                      console.log(err);
                      reject();
                    });
                } else {
                  resolve();
                }
              })
              .catch(err => {
                console.log(err);
                reject();
              });
          } else {
            resolve();
          }
        });
      }
      const main = async ()=> {
        await uploadQuestionImage()
          .then(() => {
            this.$store
              .dispatch("question/createQuestion", { questionInput: this.question })
              .then(() => {
                this.$store.dispatch("question/fetchQuestionList");
                this.dialog = false;
              });
          })
          .catch(err => {
            console.log(err);
          });
      }
      main();
    },
    onSentenceImageChange() {
      if (this.sentenceImage != null) {
        this.question.sentence.text = this.question.sentence.text + '<image>';
      } else {
        this.question.sentence.text = this.question.sentence.text.replace('<image>', '');
      }
    },
    onAnswerImageChange() {
      if (this.answerImage != null) {
        this.question.answer.text = this.question.answer.text + '<image>';
      } else {
        this.question.answer.text = this.question.answer.text.replace('<image>', '');
      }
    },
    onCommentaryImageChange() {
      if (this.commentaryImage != null) {
        this.question.commentary.text = this.question.commentary.text + '<image>';
      } else {
        this.question.commentary.text = this.question.commentary.text.replace('<image>', '');
      }
    }
  }
};
</script>
