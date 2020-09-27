<template>
  <v-content class="pt-5">
    <h3 align="center">
      ご登録のメールアドレス宛に
      「認証コード」をお送りします。
    </h3>
    <div
      v-if="isFailure"
      :class="error_class"
      align="center"
    >
      認証コードが間違っています。
      <br>再度入力してください。
    </div>
    <v-form
      ref="form"
      v-model="inputFormIsValid"
    >
      <v-text-field
        v-model="email"
        outlined
        prepend-icon="mdi-email"
        label="メールアドレス"
        :rules="[rules.required, rules.email]"
      />
    </v-form>
    <v-btn
      color="yellow darken-1"
      large
      block
      :disabled="!inputFormIsValid"
      @click="forgotPassword"
    >
      コードを送信する
    </v-btn>
    <v-btn
      color="grey darken-2"
      large
      block
      outlined
      @click="toUserLogin()"
    >
      戻る
    </v-btn>
  </v-content>
</template>

<script>
import { Auth } from "aws-amplify";
import "@mdi/font/css/materialdesignicons.css";
export default {
  name: "PasswordForgot",
  data() {
    return {
      isFailure: false,
      error_class: "alert",
      email: "",
      rules: {
        required: value => !!value || "入力されていません",
        email: value =>
          /.+@.+\..+/.test(value) || "メールアドレスの形式が正しくありません"
      },
      inputFormIsValid: false
    };
  },
  methods: {
    forgotPassword() {
      this.inputFormIsValid = this.$refs.form.validate();
      if (this.inputFormIsValid === false) return;
      Auth.forgotPassword(this.email);
      this.$router.push({
        path: "/passwordReset",
        query: { email: this.email }
      });
    },
    toUserLogin() {
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
