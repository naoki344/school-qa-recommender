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
        fluid
        fill-height
      >
        <v-layout justify-center>
          <v-flex
            xs12
            sm8
            md4
          >
            <userVerify />
          </v-flex>
        </v-layout>
      </v-container>
    </v-content>
  </v-app>
</template>



<script>
// @ is an alias to /src
import userVerify from "@/components/user/userVerify.vue";

export default {
  name: "UserVerifyPage",
  components: {
    userVerify
  }
};
</script>

