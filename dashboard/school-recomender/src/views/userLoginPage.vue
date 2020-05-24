<template>
  <v-app>
    <v-toolbar
      fixed
      style="flex: none;"
      color="yellow darken-1"
    >
      <v-toolbar-title style="width: 100%; display: flex; padding: 0; justify-content: center;">
        <img src="@/assets/toi-toy-logo-wide-s--no-border-small.png">
      </v-toolbar-title>
    </v-toolbar>
    <v-content>
      <v-container
        class="pa-4"
        fluid
        fill-height
      >
        <v-layout justify-center>
          <v-flex
            xs12
            sm8
            md4
          >
            <keep-alive>
              <component
                :is="currentView"
                @switch="switchComponent"
              />
            </keep-alive>
          </v-flex>
        </v-layout>
      </v-container>
    </v-content>
  </v-app>
</template>

<script>
// @ is an alias to /src
import userLogin from "@/components/user/userLogin.vue";
import userSignUp from "@/components/user/userSignUp.vue";

export default {
  name: "UserLoginPage",
  components: {
    userLogin,
    userSignUp
  },
  data() {
    return {
      currentView: "userLogin"
    };
  },
  methods: {
    switchComponent() {
      this.currentView =
        this.currentView == "userLogin" ? "userSignUp" : "userLogin";
      console.log("完了");
    }
  }
};
</script>
