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
          <invite />
        </v-flex>
      </v-layout>
    </v-container>
  </v-content>
</template>

<script>
// @ is an alias to /src
import invite from "@/components/user/invite.vue";

export default {
  name: "InvitePage",
  components: {
    invite
  }
};
</script>
