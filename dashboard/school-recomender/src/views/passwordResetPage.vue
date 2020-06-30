<template>
  <v-app>
    <v-app-bar
      fixed
      app
      style="flex: none;"
      color="yellow darken-1"
    >
      <v-toolbar-title style="width: 100%; display: flex; padding: 0; justify-content: center;">
        <img src="@/assets/toi-toy-logo-wide-s--no-border-small.png">
      </v-toolbar-title>
    </v-app-bar>
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
            <password-reset />
          </v-flex>
        </v-layout>
      </v-container>
    </v-content>
  </v-app>
</template>

<script>
// @ is an alias to /src
import passwordReset from "@/components/user/passwordReset.vue";
export default {
  name: "PasswordReset",
  components: {
    passwordReset
  }
};
</script>
