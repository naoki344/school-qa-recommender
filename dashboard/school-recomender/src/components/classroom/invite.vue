<template>
  <v-content class="pt-0">
    <v-container
      v-if="classroom.name != ''"
    >
      <v-row
        justify="center"
        class="mb-6 mt-12"
      >
        <v-img
          max-width="180px"
          src="@/assets/toi-toy-logo-wide-s--no-border-small.png"
        />
      </v-row>
      <div
        style="height: 70px;"
        class="mb-6"
      >
        <div
          v-if="errorMessage"
          class="alert-message"
          align="center"
        >
          参加リクエストに失敗しました。
          <br>再度実行してください。
        </div>
        <div
          v-if="successMessage"
          class="success-message"
          align="center"
        >
          参加リクエストを送信しました。
          <br>オーナーの承認をお待ちください。
        </div>
      </div>
      <v-row justify="center">
        <div>
          <h2>「{{ classroom.name }}」に参加する</h2>
          <p
            align="center"
            class="ma-0"
          >
            {{ classroom.caption }}
          </p>
        </div>
      </v-row>
      <v-row justify="center">
        <v-col cols="7">
          <div
            v-for="(owner, index) in classroom.owner_list"
            :key="index"
            class="ma-1"
          >
            <v-avatar
              tile
              size="25"
              style="border-radius: 6px;"
            >
              <v-img :src="getUserAvatarImageUrl(owner.user_id)" />
            </v-avatar>
            <p class="font-weight-bold ma-2 owner-name">
              {{ owner.nickname }}
            </p>
          </div>
        </v-col>
      </v-row>
    </v-container>
    <v-btn
      v-if="canJoinRequest"
      block
      color="yellow darken-1"
      large
      @click="join"
    >
      <strong class="login">参加する</strong>
    </v-btn>
    <v-btn
      v-if="toTopPage"
      block
      color="yellow darken-1"
      large
      @click="goToTopPage"
    >
      <strong class="login">トップページへ</strong>
    </v-btn>
    <v-dialog
      v-model="unSignUpDialog"
      width="360px"
    >
      <v-card style="texta">
        <v-card-title>
          <v-spacer />
          <v-img
            max-width="180px"
            src="@/assets/toi-toy-logo-wide-s--no-border-small.png"
          />
          <v-spacer />
        </v-card-title>
        <v-card-text class="px-3 py-4">
          <p style="text-align: center;">
            <strong>ログインもしくはユーザー登録をしてください</strong>
          </p>
        </v-card-text>
        <v-card-actions class="justify-space-around">
          <v-btn
            color="yellow darken-1"
            @click="goToSignUpPage"
          >
            ユーザー登録
          </v-btn>
          <v-btn
            color="yellow darken-1"
            @click="goToLoginPage"
          >
            ログイン
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-content>
</template>

<script>
export default {
  name: "Invite",
  data: () => ({
    classroom: {
      name: "",
      caption: "",
      owner_list: []
    },
    successMessage: false,
    errorMessage: false,
    canJoinRequest: true,
    toTopPage: false,
    unSignUpDialog: false,
  }),
  computed: {
    inviteKey() {
      return this.$route.query.inviteKey;
    }
  },
  created() {
    this.$store
      .dispatch("classroom/fetchClassroomByInviteKey", this.inviteKey)
      .then(data => {
        this.classroom = data;
      })
      .catch(err => {
        console.log(err);
      });
  },
  methods: {
    async join() {
      const isLogin = await this.$store.getters["user/isLogin"];
      if (!isLogin) {
        this.unSignUpDialog = true;
	  } else {
        this.errorMessage = false
        this.$store
          .dispatch("classroom/joinRequestByinviteKey", this.inviteKey)
          .then(data => {
            this.successMessage = true
            this.canJoinRequest = false
            this.toTopPage = true
          })
          .catch(err => {
            this.errorMessage = true
          });
      }
    },
    getUserAvatarImageUrl(userId) {
      return this.$store.getters["user/userAvatarImageUrl"](userId);
    },
    goToTopPage() {
      this.$router.push({ path: "/" });
    },
    goToLoginPage() {
      this.$router.push({ path: "/userLogin", query: {originPagePath: this.$route.fullPath} });
    },
    goToSignUpPage() {
      this.$router.push({ path: "/userSignUp", query: {originPagePath: this.$route.fullPath} });
    }
  }
};
</script>

<style lang="scss" scoped>
.owner-name {
  display: inline-block;
}
.login {
  font-size: 20px;
}
.alert-message {
  background-color: #fcc;
  padding: 10px;
  border: 1px solid #f33;
}
.success-message {
  background-color: #e6f4e5;
  padding: 10px;
  border: 1px solid #4caf50;
}
</style>
