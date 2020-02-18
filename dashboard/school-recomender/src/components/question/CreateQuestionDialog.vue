<template>
  <v-item>
    <v-card
      class="d-flex align-center"
      height="200"
    >
      <v-row justify="center">
        <v-dialog v-model="dialog" persistent width="90%">
          <template v-slot:activator="{ on }">
            <v-btn color="green" dark v-on="on">新しい問いを追加</v-btn>
          </template>
          <v-card>
            <v-card-title class="headline">新しい問いを作成する</v-card-title>
            <v-card-text>問題の形式をタブから選び、問いおよび回答を入力してください。</v-card-text>
            <v-tabs :vertical="false">

              <v-tab><v-icon left>mdi-grease-pencil</v-icon>記述式</v-tab>
              <v-tab-item>
                <v-card flat>
                  <v-card-text>
                    <v-container fluid>
                      <v-row align="center">
                        <v-col cols="4" md=2 lg=2>
                          <v-subheader>教科</v-subheader>
                        </v-col>
                        <v-col cols="8" md=2 lg=2>
                          <v-select
                            v-model="question.subjectName"
                            :items="subjectList"
                            menu-props="auto"
                            label="Select"
                            hide-details
                            single-line
                          ></v-select>
                        </v-col>
                        <v-col cols="4" md=2 lg=2>
                          <v-subheader>回答時間(目安)</v-subheader>
                        </v-col>
                        <v-col cols="2" md=2 lg=2>
                          <v-select
                            v-model="question.estimatedTime"
                            :items="timeList"
                            menu-props="auto"
                            label="Select"
                            hide-details
                            single-line
                          ></v-select>
                        </v-col>
                     </v-row>
                      <v-row>
                        <v-col cols="4" md=2 lg=2>
                          <v-subheader>分類タグ</v-subheader>
                        </v-col>
                        <v-col cols="4" md=6 lg=6>
                          <v-combobox
                            v-model="question.sortTagList"
                            :items="tagItems"
                            label="I use chips"
                            multiple
                            chips
                          ></v-combobox>
                        </v-col>
                      </v-row>
                      <v-row align="center">
                        <v-col cols="10" md=9 lg=9>
                          <v-textarea
                            v-model="question.sentence.text"
                            label="問い"
                            required
                          ></v-textarea>
                        </v-col>
                        <v-col clos="2" md=3 lg=3>
                          <v-file-input chips label="問い画像"></v-file-input>
                        </v-col>
                      </v-row>
                      <v-row align="center">
                        <v-col cols="10" md=9 lg=9>
                          <v-textarea
                            v-model="question.answer.text"
                            label="模範回答"
                            required
                          ></v-textarea>
                        </v-col>
                        <v-col clos="2" md=3 lg=3>
                          <v-file-input chips label="模範回答画像"></v-file-input>
                        </v-col>
                      </v-row>
                      <v-row align="center">
                        <v-col cols="10" md=9 lg=9>
                          <v-textarea
                            v-model="question.commentary.text"
                            label="解説"
                            required
                          ></v-textarea>
                        </v-col>
                        <v-col clos="2" md=3 lg=3>
                          <v-file-input chips label="解説画像"></v-file-input>
                        </v-col>
                      </v-row>
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
              <v-btn color="green darken-1" text @click="dialog = false">閉じる</v-btn>
              <v-btn color="green darken-1" @click="createQuestion">送信</v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
      </v-row>
    </v-card>
  </v-item>
</template>

<script>
  export default {
    name: 'CreateQuestionDialog',
    data: () => ({
      dialog: false,
      subjectList: ["数学", "英語", "国語", "社会"],
      tagItems: ["因数分解", "初級"],
      timeList: [1, 3, 5, 15, 30, 60],
      question: {
        subjectName: '',
        estimatedTime: '',
        sentence: {text: ''},
        answer: {text: ''},
        commentary: {text: ''},
        sortTagList: [],
      },
      select: [],
    }),
    methods: {
      createQuestion() {
        this.$store.dispatch('createQuestion', {questionInput: this.question})
      },
    },
  }
</script>
