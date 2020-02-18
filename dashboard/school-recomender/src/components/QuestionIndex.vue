<template>
  <v-container>
    <v-layout row wrap>
      <v-flex xs12 sm6 style="margin: 10px;">
        <v-text-field
          v-model="username"
          counter="25"
          hint="ユーザー作成時のメールアドレスを入力"
          label="メールアドレス"
        ></v-text-field>
      </v-flex>
      <v-flex xs12 sm6 style="margin: 10px;">
        <v-text-field
          v-model="password"
          :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
          :type="showPassword ? 'text' : 'password'"
          name="input-10-1"
          label="パスワードを入力"
          counter
          @click:append="showPassword = !showPassword"
        ></v-text-field>
      </v-flex>
    </v-layout>
    <v-btn color="green darken-1" @click="userLogin">ログイン</v-btn>
    <v-btn color="green darken-1" @click="fetchQuestionList">問い一覧の取得</v-btn>
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
            v-for="question in questionCardList"
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
                  <div>{{question.register_date | dateTimeFilter}} ({{question.register_user_id}})</div>
                  <v-chip class="" small color="green" text-color="white" style="padding-left: 6px;">
                    <v-avatar left class="green darken-4">{{question.estimated_time}}</v-avatar>
                    Min
                  </v-chip>
                  </div>
                  <h2 class="mb-1" style="size: 20px;">
                    【{{question.subject_type | subjectTypeFilter}}】{{question.sort_tag_list | sortTagListFilter}}</h2>
                  <p>{{question.question_type | questionTypeFilter}}</p>
                  <div class="text--primary">{{question.question_sentence.text}}</div>
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
  import { mapState } from 'vuex';
  import moment from "moment";
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
      username: '',
      password: '',
      showPassword: false,
      mandatory: false,
      multiple: true,
      dialog: false,
      questionList: []
    }),
    computed: {
      ...mapState({
        questionCardList: state => state.questionCardList
      }),
    },
    methods: {
      fetchQuestionList() {
        this.$store.dispatch('fetchQuestionList')
      },
      userLogin() {
        this.$store.dispatch('userLogin', {
          "username": this.username,
          "password": this.password
        });
      },
    },
    filters: {
      subjectTypeFilter: function (value) {
        if (!value) return '';
        if (value === 'math') return '数学';
        return '';
      },
      questionTypeFilter: function (value) {
        if (!value) return '';
        if (value === 'describing') return '記述式';
        if (value === 'selectable') return '選択式';
        return '';
      },
      dateTimeFilter: function (value) {
        if (!value) return '';
        return moment(value).format('MM月DD日 hh:mm');
      },
      sortTagListFilter: function (value) {
        if (!value) return '';
        return value.join(',');
      },
    }
  }
</script>
