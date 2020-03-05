<template>
  <v-item>
    <v-card class="d-flex align-center" height="200">
      <v-row justify="center">
        <v-dialog v-model="dialog" persistent width="90%">
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
                            <v-subheader>回答時間(目安)</v-subheader>
                          </v-col>
                          <v-col cols="2" md="2" lg="2">
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
                            <v-subheader>分類タグ</v-subheader>
                          </v-col>
                          <v-col cols="4" md="6" lg="6">
                            <v-combobox
                              v-model="question.sortTagList"
                              :items="tagItems"
                              label="分類を入力(複数入力、自由作成可)"
                              multiple
                              required
                              chips
                            ></v-combobox>
                          </v-col>
                        </v-row>
                        <v-row align="center">
                          <v-col cols="10" md="9" lg="9">
                            <v-textarea
                              v-model="question.sentence.text"
                              label="問い"
                              required
                            ></v-textarea>
                          </v-col>
                          <v-col clos="2" md="3" lg="3">
                            <v-file-input chips label="問い画像"></v-file-input>
                          </v-col>
                        </v-row>
                        <v-row align="center">
                          <v-col cols="10" md="9" lg="9">
                            <v-textarea
                              v-model="question.answer.text"
                              label="模範回答"
                              required
                            ></v-textarea>
                          </v-col>
                          <v-col clos="2" md="3" lg="3">
                            <v-file-input
                              chips
                              label="模範回答画像"
                            ></v-file-input>
                          </v-col>
                        </v-row>
                        <v-row align="center">
                          <v-col cols="10" md="9" lg="9">
                            <v-textarea
                              v-model="question.commentary.text"
                              label="解説"
                              required
                            ></v-textarea>
                          </v-col>
                          <v-col clos="2" md="3" lg="3">
                            <v-file-input chips label="解説画像"></v-file-input>
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
              <v-btn color="green darken-1" @click="createQuestion">送信</v-btn>
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
    dialog: false,
    subjectList: schoolApiQuesionTransfer.getSubjectNameList(),
    tagItems: ["因数分解", "初級"],
    timeList: [1, 3, 5, 15, 30, 60],
    subjectNameRules: [v => !!v || "教科を選択してください"],
    estimatedTimeRules: [v => !!v || "目安時間を選択してください"],
    question: {
      subjectName: "",
      questionType: "describing",
      estimatedTime: "",
      sentence: { text: "" },
      answer: { text: "" },
      commentary: { text: "" },
      sortTagList: []
    },
    select: [],
    valid: true
  }),
  methods: {
    createQuestion() {
      if (this.$refs.form.validate()) {
        this.snackbar = true;
      } else {
        this.valid = false;
        return;
      }
      this.$store
        .dispatch("question/createQuestion", { questionInput: this.question })
        .then(() => {
          this.$store.dispatch("question/fetchQuestionList");
          this.dialog = false;
        });
    }
  }
};
</script>
