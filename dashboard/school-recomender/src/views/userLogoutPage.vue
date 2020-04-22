<template>
  <v-app>
    <v-content />
  </v-app>
</template>

<script>
// @ is an alias to /src
import userLogin from "@/components/user/userLogin.vue";

export default {
  name: "UserLogoutPage",
  mounted() {
    this.$store.dispatch("user/userLogout")
      .then((question) => {
        this.$router.push({ path: "/userLogin" });
      })
      .catch((err) => {
        this.$router.push({ path: "/" });
      });
  }
};
</script>

