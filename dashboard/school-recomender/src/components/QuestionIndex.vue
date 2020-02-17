<template>
  <v-container>
    <v-btn color="green darken-1" @click="fetchQuestionList">送信</v-btn>
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
                    <v-avatar left class="green darken-4">{{question.estimated_time}}</v-avatar>
                    Min
                  </v-chip>
                  </div>
                  <h2 class="mb-1" style="size: 20px;">【{{question.subject_type}}】</h2>
                  <p>{{question.question_type}}</p>
                  <div class="text--primary">{{question.sentence_summary}}</div>
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
  import schoolApiClient from '../api/common.js';
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
        {question_id: 1, subject_type: "数学", sort_tag_list: "因数分解", sentence_summary: "[I] a3−b3=(a−b)(a2+ab+b2)<br>", register_user_id: "三好 直紀", register_date: "2020年 12月10日", question_type: "記述式", estimated_time: "10"},
      ]
    }),
    methods: {
      fetchQuestionList() {
        const cognitoConfig = {
          region: process.env.VUE_APP_REGION,
          userPoolId: process.env.VUE_APP_COGNITO_USER_POOL_ID,
          appClientId: process.env.VUE_APP_COGNITO_APP_CLIENT_ID,
          adminIdentifyPoolId: process.env.VUE_APP_ADMIN_IDENTITY_POOL_ID,
          adminLoginsKey: process.env.VUE_APP_ADMIN_LOGINS_KEY
        }
        const cognitoUser = schoolApiClient.loginUser(cognitoConfig, {
          Username: "trombone344@gmail.com",
          Password: "q?J5kF"
        });
        const pathTemplate = '/devmiyoshi/admin/question'
        const pathParams = {};
        schoolApiClient.fetchRestAPI(
          cognitoConfig, cognitoUser, "GET", pathTemplate, pathParams, {}, {}
         ).then((result) => {
           this.questionList = result.data["question_card_list"];
           console.log(result.data["question_card_list"]);
           });
      },
    },
  }
</script>
