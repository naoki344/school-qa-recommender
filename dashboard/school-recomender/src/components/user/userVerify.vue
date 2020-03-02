<template>
  <v-card class="elevation-6">
    <v-toolbar color="yellow darken-1" flat>
      <v-spacer></v-spacer>
      <v-toolbar-title>
        <strong>ユーザー認証画面</strong>
      </v-toolbar-title>
      <v-spacer></v-spacer>
    </v-toolbar>
    <v-card-text>
      <div v-if="isFailure" v-bind:class="error_class">
        認証コードが間違っています。
        再度入力してください。
      </div>
      <v-text-field v-model="email" prepend-icon label="メールアドレス" required></v-text-field>
      <v-text-field v-model="verificationCode" prepend-icon label="認証コード" required></v-text-field>
    </v-card-text>
    <v-card-actions>
      <v-spacer></v-spacer>
      <v-btn color="yellow darken-1" @click="userVerify" block>認証する</v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
import "@mdi/font/css/materialdesignicons.css";
export default {
  name: "userVerify",
  data: () => ({
    email: "",
    verificationCode: "",
    isFailure: false,
    error_class: "alert"
  }),
  methods: {
    userVerify() {
      this.$store
        .dispatch("userVerify", {
          email: this.email,
          verificationCode: this.verificationCode
        })
        .then(() => {
          this.$router.push({ path: "/userLogin" });
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