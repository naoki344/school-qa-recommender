<template>
  <v-app>
    <v-content>
      <v-container
        fluid
        class="pa-0"
      >
        <keep-alive :include="cacheComponentName">
          <router-view />
        </keep-alive>
      </v-container>
    </v-content>
  </v-app>
</template>

<script>
export default {
  data() {
    return {
      cacheComponentName: ["TopPage", "UserLoginPage", "UserSignUpPage"]
    };
  },
  computed: {
    isLogin() {
      return this.$store.getters["user/isLogin"];
    }
  },
  async created() {
    await this.$store.dispatch("user/fetchLoginUserInfo");
  }
};
</script>

<style lang="scss">
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}

#nav {
  padding: 30px;

  a {
    font-weight: bold;
    color: #2c3e50;

    &.router-link-exact-active {
      color: #42b983;
    }
  }
}
</style>
