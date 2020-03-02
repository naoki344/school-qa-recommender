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
      <v-form>
        <v-text-field
          v-model="username"
          prepend-icon="mdi-email"
          counter="25"
          hint="ユーザー作成時のメールアドレスを入力"
          label="メールアドレス"
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
    showPassword: false
  }),
  methods: {
    userLogin() {
      this.$store
        .dispatch("userLogin", {
          username: this.username,
          password: this.password
        })
        .then(() => {
          this.$router.push({ path: "/" });
        })
        .catch(err => {
          console.log(err);
        });
    }
  }
};
</script>

