<template>
  <v-content class="pt-5">
    <h3 align="center">
      ご登録のメールアドレス宛にお送りした認証コードと新しいメールアドレスを記入してください。
    </h3>

    <div
      v-if="isFailure"
      :class="error_class"
      align="center"
    >
      認証コードが間違っています。
      <br>再度入力してください。
    </div>
    <v-text-field
      v-model="email"
      prepend-icon
      label="メールアドレス"
      required
    />
    <v-text-field
      v-model="code"
      prepend-icon
      label="認証コード"
      required
    />
    <v-text-field
      v-model="newPassword"
      prepend-icon
      label="新しいパスワード"
      required
    />
    <v-btn
      color="yellow darken-1"
      block
      large
      @click="passwordReset"
    >
      パスワードをリセットする
    </v-btn>
  </v-content>
</template>

<script>
import { Auth } from "aws-amplify";
import "@mdi/font/css/materialdesignicons.css";
export default {
  name: "PasswordReset",
  data() {
    return {
      isFailure: false,
      error_class: "alert",
      email: "",
      code: "",
      newPassword: ""
    };
  },
  methods: {
    passwordReset() {
      Auth.forgotPasswordSubmit(this.email, this.code, this.newPassword);
      this.$router.push({ path: "/userLogin" });
    }
  }
};
</script>

<style lang="scss" scoped >
.alert {
  background-color: #fcc;
  padding: 10px;
  border: 1px solid #f33;
}
</style>
