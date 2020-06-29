<template>
  <v-content class="pt-5">
    <h3 align="center">ご登録のメールアドレス宛にお送りした認証コードと新しいメールアドレスを記入してください。</h3>

    <div v-if="isFailure" :class="error_class" align="center">
      認証コードが間違っています。
      <br />再度入力してください。
    </div>
    <v-form ref="form" v-model="inputFormIsValid">
      <v-text-field
        v-model="email"
        outlined
        name="email"
        label="メールアドレス"
        prepend-icon="mdi-email"
        required
        hint="メールアドレスを入力"
        :rules="[rules.required, rules.email]"
        @keydown.prevent.enter="moveNext"
      />
      <v-text-field
        v-model="code"
        outlined
        :rules="[
          rules.required,
        ]"
        label="認証コード"
        required
      />
      <v-text-field
        v-model="password"
        name="password"
        label="新しいパスワード"
        prepend-icon="mdi-key"
        outlined
        counter
        required
        :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
        :type="showPassword ? 'text' : 'password'"
        :rules="[rules.required, rules.password]"
        @keydown.prevent.enter="moveNext"
        @click:append="showPassword = !showPassword"
        @change="passwordValidation"
      />
      <v-text-field
        ref="passwordConfirm"
        v-model="passwordConfirm"
        name="password-confirm"
        label="新しいパスワード(確認)"
        prepend-icon="mdi-key"
        outlined
        counter
        :append-icon="showPasswordConfirm ? 'mdi-eye' : 'mdi-eye-off'"
        :type="showPasswordConfirm ? 'text' : 'password'"
        :rules="[
          rules.required,
          rules.password,
          v => v === password || 'パスワードが一致していません'
        ]"
        @click:append="showPasswordConfirm = !showPasswordConfirm"
      />
    </v-form>
    <v-btn
      color="yellow darken-1"
      block
      large
      :disabled="!inputFormIsValid"
      @click="passwordReset"
    >パスワードをリセットする</v-btn>
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
      code: "",
      password: "",
      passwordConfirm: "",
      inputFormIsValid: false,
      showPassword: false,
      showPasswordConfirm: false,
      rules: {
        required: value => !!value || "入力されていません",
        email: value =>
          /.+@.+\..+/.test(value) || "メールアドレスの形式が正しくありません",
        password: value =>
          /^(?=.*?[a-z])(?=.*?\d)(?=.*?[!-\/:-@[-`{-~])[!-~]{6,100}$/.test(
            value
          ) || "パスワードには、大文字、小文字、記号を使用してください"
      }
    };
  },
  computed: {
    email() {
      return this.$route.query.email;
    }
  },
  methods: {
    passwordReset() {
      this.inputFormIsValid = this.$refs.form.validate();
      if (this.inputFormIsValid === false) return;
      Auth.forgotPasswordSubmit(this.email, this.code, this.password);
      this.$router.push({ path: "/userLogin" });
    },
    passwordValidation() {
      if (this.$refs.form == null) return;
      this.$refs.passwordConfirm.validate();
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
      if (event.keyCode !== 13) {
        return;
      }
      const index = this.findIndex(event.target);
      this.moveFocus(index + 1);
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
