<template>
  <v-card class="elevation-6" height="300">
    <v-toolbar color="yellow darken-1" flat>
      <v-spacer></v-spacer>
      <v-toolbar-title>
        <strong>Toi-Toy</strong>
      </v-toolbar-title>
      <v-spacer></v-spacer>
    </v-toolbar>
    <v-card-text>
      <v-text-field v-model="email" prepend-icon label="メールアドレス" required></v-text-field>
      <v-text-field v-model="verificationCode" prepend-icon label="認証コード" required></v-text-field>
    </v-card-text>
    <v-card-actions>
      <v-spacer></v-spacer>
      <v-btn color="yellow darken-1" @click="userConfirm">認証する</v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
import "@mdi/font/css/materialdesignicons.css";
export default {
  name: "userConfirm",
  data: () => ({
    email: '',
    verificationCode: '',
  }),
  methods: {
    userConfirm() {
      this.$store
        .dispatch("userConfirm", {
          email: this.email,
          verificationCode: this.verificationCode
        })
        .then(() => {
          this.$router.push({ path: "/userLogin" });
        })
        .catch(err => {
          console.log(err);
        });
    }
  }
};
</script>

