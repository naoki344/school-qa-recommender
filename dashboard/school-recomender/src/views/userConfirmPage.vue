<template>
  <v-app>
    <v-content>
      <v-container fluid fill-height>
        <v-layout align-center justify-center>
          <v-flex xs12 sm8 md4>
            <userConfirm />
          </v-flex>
        </v-layout>
      </v-container>
    </v-content>
  </v-app>
</template>

<script>
// @ is an alias to /src
import userConfirm from "@/components/user/userConfirm.vue";

export default {
  name: "userConfirmPage",
  components: {
    userConfirm
  }
};
</script>

