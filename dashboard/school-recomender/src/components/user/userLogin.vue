<template>
  <v-card class="elevation-6">
    <v-toolbar color="yellow darken-1" flat>
      <v-spacer></v-spacer>
      <v-toolbar-title>
        <strong>Toi-Toyにログイン</strong>
      </v-toolbar-title>
      <v-spacer></v-spacer>
    </v-toolbar>
    <v-card-text>
      <p v-if="error" class="alert">メールアドレス または パスワードが間違っています</p>
      <v-form>
        <v-text-field
          v-model="username"
          prepend-icon="mdi-email"
          counter="25"
          hint="ユーザー作成時のメールアドレスを入力"
          label="メールアドレス"
          required
        ></v-text-field>
        <v-text-field
          v-model="password"
          :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
          :type="showPassword ? 'text' : 'password'"
          name="input-10-1"
          prepend-icon="mdi-key"
          label="パスワードを入力"
          counter
          @click:append="showPassword = !showPassword"
          required
        ></v-text-field>
      </v-form>
    </v-card-text>
    <v-card-actions>
      <v-spacer></v-spacer>
      <v-btn color="yellow darken-1" @click="userLogin" x-large block>ログイン</v-btn>
    </v-card-actions>
  </v-card>
</template>



<script>
import "@mdi/font/css/materialdesignicons.css";
export default {
  name: "Login",
  data: () => ({
    username: "",
    password: "",
    showPassword: false,
    error: false
  }),
  methods: {
    userLogin() {
      this.$store
        .dispatch("user/userLogin", {
          username: this.username,
          password: this.password
        })
        .then(() => {
          this.$router.push({ path: "/" });
        })
        .catch(err => {
          console.log(err);
          this.error = true;
          this.password = "";
        });
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
