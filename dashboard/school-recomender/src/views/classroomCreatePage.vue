<template>
  <v-app>
    <v-content>
      <v-container fluid fill-height>
        <v-layout align-center justify-center>
          <v-flex xs12 sm8 md4>
            <classroomCreate />
          </v-flex>
        </v-layout>
      </v-container>
    </v-content>
  </v-app>
</template>

<script>
// @ is an alias to /src
import classroomCreate from "@/components/classroom/classroomCreate.vue";

export default {
  name: "classroomCreatePage",
  components: {
    classroomCreate
  }
};
</script>
