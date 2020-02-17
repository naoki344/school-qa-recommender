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
                        <v-col cols="4" md=1 lg=1>
                          <v-subheader>教科</v-subheader>
                        </v-col>
                        <v-col cols="8" md=2 lg=2>
                          <v-select
                            v-model="e1"
                            :items="subjectList"
                            menu-props="auto"
                            label="Select"
                            hide-details
                            single-line
                          ></v-select>
                        </v-col> 
                        <v-col cols="4" md=1 lg=1>
                          <v-subheader>回答時間(目安)</v-subheader>
                        </v-col>
                        <v-col cols="1" md=1 lg=1>
                          <v-select
                            v-model="e1"
                            :items="timeList"
                            menu-props="auto"
                            label="Select"
                            hide-details
                            single-line
                          ></v-select>
                        </v-col> 
                     </v-row>
                      <v-row>
                        <v-col cols="4" md=1 lg=1>
                          <v-subheader>分類タグ</v-subheader>
                        </v-col>
                        <v-col cols="4" md=4 lg=4>
                          <v-combobox
                            v-model="select"
                            :items="tagItems"
                            label="I use chips"
                            multiple
                            chips
                          ></v-combobox>
                        </v-col>
                        <v-col cols="4" md=1 lg=1>
                          <v-subheader>画像</v-subheader>
                        </v-col>
                        <v-col clos="4" md=4>
                          <v-file-input chips label="添付したい画像を洗濯してください"></v-file-input>
                        </v-col>
                      </v-row>
                      <v-textarea
                        :value="question"
                        label="問い"
						required
                      ></v-textarea>
                      <v-textarea
                        label="模範解答"
                      ></v-textarea>
                      <v-textarea
                        label="解説"
                      ></v-textarea>
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
              <v-btn color="green darken-1" @click="postApi">送信</v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
      </v-row>
    </v-card>
  </v-item>
</template>

<script>
  import schoolApiClient from '../../api/common.js';
  export default {
    name: 'CreateQuestionDialog',
    data: () => ({
      dialog: false,
      subjectList: ["数学", "英語", "国語", "社会"],
      tagItems: ["因数分解", "初級"],
      timeList: [1, 3, 5, 15, 30, 60],
      question: "以下の問いに答えなさい\n {image}",
      e1: [],
      select: [],
    }),
    methods: {
      postApi() {
        const cognitoConfig = {
          region: process.env.VUE_APP_REGION,
          userPoolId: process.env.VUE_APP_COGNITO_USER_POOL_ID,
          appClientId: process.env.VUE_APP_COGNITO_APP_CLIENT_ID,
          adminIdentifyPoolId: process.env.VUE_APP_ADMIN_IDENTITY_POOL_ID,
          adminLoginsKey: process.env.VUE_APP_ADMIN_LOGINS_KEY
        }
        const cognitoUser = schoolApiClient.loginUser(cognitoConfig, {
          Username: "",
          Password: ""
        });
        const pathTemplate = '/devmiyoshi/admin/question/{QuestionId}'
        const pathParams = {
          QuestionId: '1',
        };
        schoolApiClient.fetchRestAPI(
          cognitoConfig, cognitoUser, "GET", pathTemplate, pathParams, {}, {}
		).then((result) => {this.question = JSON.stringify(result.data)});
      },
    },
  }
</script>
