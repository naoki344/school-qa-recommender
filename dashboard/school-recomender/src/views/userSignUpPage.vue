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
        class="pa-6"
        fluid
        fill-height
      >
        <v-layout justify-center>
          <v-flex
            xs12
            sm8
            md4
          >
            <userSignUp />
          </v-flex>
        </v-layout>
      </v-container>
    </v-content>
  </v-app>
</template>

<script>
// @ is an alias to /src
import userSignUp from "@/components/user/userSignUp.vue";

export default {
  name: "UserSignUpPage",
  components: {
    userSignUp
  },
};
</script>
