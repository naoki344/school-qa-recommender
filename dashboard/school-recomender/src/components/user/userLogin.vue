<template>
  <v-content class="pt-0">
    <h1 align="center">
      ログイン
    </h1>
    <h5 align="center">
      または
      <a @click="toUserSignUp">アカウントを作る</a>
    </h5>

    <p
      v-if="error"
      class="alert"
    >
      メールアドレス または パスワードが間違っています
    </p>
    <v-form class="pt-3">
      <v-text-field
        v-model="username"
        outlined
        class="user-login-input-form"
        prepend-icon="mdi-email"
        hint="ユーザー作成時のメールアドレスを入力"
        label="メールアドレス"
        required
        @keydown.prevent.enter="moveNext"
      />
      <v-text-field
        v-model="password"
        outlined
        class="user-login-input-form"
        required
        :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
        :type="showPassword ? 'text' : 'password'"
        name="input-10-1"
        prepend-icon="mdi-key"
        label="パスワード"
        counter
        @keydown.enter="userLogin"
        @click:append="showPassword = !showPassword"
      />
    </v-form>
    <p>
      パスワードを忘れた方は
      <a @click="toForgotPassword">こちら</a>
    </p>
    <v-spacer />
    <v-btn
      block
      color="yellow darken-1"
      large
      class="user-login-input-form"
      :loading="loading"
      :disabled="loading"
      @click="userLogin"
    >
      ログインする
    </v-btn>
  </v-content>
</template>

<script>
import "@mdi/font/css/materialdesignicons.css";
export default {
  name: "UserLogin",
  data: () => ({
    username: "",
    password: "",
    showPassword: false,
    error: false,
    loading: false
  }),
  computed: {
    originPagePath() {
      return this.$route.query.originPagePath;
    }
  },
  methods: {
    toUserSignUp() {
      if (this.originPagePath == undefined || this.originPagePath == null) {
        this.$router.push({ path: "/userSignUp" });
      } else {
        this.$router.push({
          path: "/userSignUp",
          query: { originPagePath: this.originPagePath }
        });
      }
    },
    toForgotPassword() {
      this.$router.push({ path: "/passwordForgot" });
    },
    userLogin() {
      this.loading = true;
      this.$store
        .dispatch("user/userLogin", {
          username: this.username,
          password: this.password
        })
        .then(() => {
          if (this.originPagePath == undefined || this.originPagePath == null) {
            this.$router.push({ path: "/" });
          } else {
            this.$router.push({ path: this.originPagePath });
          }
        })
        .catch(err => {
          console.log(err);
          this.error = true;
          this.password = "";
        });
      this.loading = false;
    },
    findIndex(target) {
      return this.elements.findIndex(
        e => e.getElementsByTagName("input")[0] === target
      );
    },
    moveFocus(index) {
      if (this.elements[index]) {
        this.elements[index].getElementsByTagName("input")[0].focus();
      }
    },
    moveNext(event) {
      if (event.keyCode !== 13) return;
      const index = this.findIndex(event.target);
      this.moveFocus(index + 1);
    }
  }
};
</script>

<style lang="scss">
.alert {
  background-color: #fcc;
  padding: 5px;
  border: 1px solid #f33;
}
</style>