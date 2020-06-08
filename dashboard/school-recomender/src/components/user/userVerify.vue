<template>
  <v-content class="pt-5">
    <h3 align="center">
      ご登録のメールアドレス宛に
      「認証コード」をお送りしました。
      メールの本文に記載されている
      「認証コード」を入力してアカウントを有効化してください。
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
      v-model="verificationCode"
      prepend-icon
      label="認証コード"
      required
    />

    <v-btn
      color="yellow darken-1"
      block
      large
      @click="userVerify"
    >
      有効化する
    </v-btn>
  </v-content>
</template>

<script>
import { mapGetter } from "vuex";
import "@mdi/font/css/materialdesignicons.css";
export default {
  name: "UserVerify",
  data: () => ({
    verificationCode: "",
    isFailure: false,
    error_class: "alert"
  }),
  computed: {
    email() {
      return this.$route.query.email;
    },
    originPagePath() {
      return this.$route.query.originPagePath;
    }
  },
  methods: {
    userVerify() {
      this.$store
        .dispatch("user/userVerify", {
          email: this.email,
          verificationCode: this.verificationCode
        })
        .then(() => {
          if (this.originPagePath == undefined || this.originPagePath == null){
            this.$router.push({ path: "/userLogin" });
          } else {
            this.$router.push({ path: "/userLogin", query: { originPagePath: this.originPagePath }});
          }
        })
        .catch(() => {
          this.isFailure = true;
        });
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
