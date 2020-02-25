<template>
  <v-app>
    <v-content>
      <v-container fluid fill-height>
        <v-layout align-center justify-center>
          <v-flex xs12 sm8 md4>
            <SignUp />
          </v-flex>
        </v-layout>
      </v-container>
    </v-content>
  </v-app>
</template>

<script>
// @ is an alias to /src
import SignUp from "@/components/user/SignUp.vue";

export default {
  name: "UserSignUp",
  components: {
    SignUp
  }
};
</script>
