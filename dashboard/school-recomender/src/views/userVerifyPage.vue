<template>
  <v-content>
    <v-container
      fluid
      fill-height
    >
      <v-layout
        align-center
        justify-center
      >
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

