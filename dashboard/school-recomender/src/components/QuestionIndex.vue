<template>
  <v-container>
    <v-item-group
      :mandatory="mandatory"
      :multiple="multiple"
    >
      <v-container class="pa-0">
        <v-row>
          <v-col cols=12 sm=12 md=6 lg=4 xl=3>
            <create-question-dialog></create-question-dialog>
          </v-col>
          <v-col
            v-for="question in questionList"
            :key="question.question_id"
            cols=12 sm=12 md=6 lg=4 xl=3
          >
            <v-item v-slot:default="{ active, toggle }">
              <v-card
                v-if="type === 'cards'"
                :color="active ? 'grey darken' : ''"
                class="d-flex align-center"
                white
                height="200"
                @click="toggle"
              >
                <v-card-text>
                  <div class="mb-2" style="display: flex; justify-content: space-between">
                  <div>{{question.register_date}} ({{question.register_user}})</div>
                  <v-chip class="" small color="green" text-color="white" style="padding-left: 6px;">
                    <v-avatar left class="green darken-4">{{question.target_time}}</v-avatar>
                    Min
                  </v-chip>
                  </div>
                  <h2 class="mb-1" style="size: 20px;">【{{question.subject}}】{{question.category}}</h2>
                  <p>{{question.question_type}}</p>
                  <div class="text--primary">{{question.contents}}</div>
                </v-card-text>
                <v-scroll-y-transition>
                  <div
                    v-if="active"
                    class="display-1 font-weight-bold"
                    style="position: absolute; right:5px; bottom:0;"
                  >
                    Add
                  </div>
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
  import '@mdi/font/css/materialdesignicons.css'
  import CreateQuestionDialog from './question/CreateQuestionDialog'
  export default {
    name: 'QuestionIndex',
	components: {
      CreateQuestionDialog,
    },
    data: () => ({
      types: [
        'cards',
        'images',
      ],
      type: 'cards',
      mandatory: false,
      multiple: true,
      dialog: false,
      questionList: [
        {question_id: 1, subject: "数学", category: "因数分解", contents: "[I] a3−b3=(a−b)(a2+ab+b2)<br>", register_user: "三好 直紀", register_date: "2020年 12月10日", question_type: "記述式", target_time: "10"},
        {question_id: 2, subject: "数学", category: "因数分解", contents: "[I] a3−b3=(a−b)(a2+ab+b2)<br>", register_user: "三好 直紀", register_date: "2020年 12月10日", question_type: "選択式", target_time: "10"},
        {question_id: 3, subject: "数学", category: "因数分解", contents: "[I] a3−b3=(a−b)(a2+ab+b2)<br>", register_user: "三好 直紀", register_date: "2020年 12月10日", question_type: "記述式", target_time: "10"},
        {question_id: 4, subject: "数学", category: "因数分解", contents: "[I] a3−b3=(a−b)(a2+ab+b2)<br>", register_user: "三好 直紀", register_date: "2020年 12月10日", question_type: "記述式", target_time: "10"},
        {question_id: 5, subject: "数学", category: "因数分解", contents: "[I] a3−b3=(a−b)(a2+ab+b2)<br>", register_user: "三好 直紀", register_date: "2020年 12月10日", question_type: "記述式", target_time: "10"},
      ]
    }),
  }
</script>
