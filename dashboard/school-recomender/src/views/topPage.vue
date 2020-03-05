<template>
  <v-app>
    <classroomSwiper />
    <v-content>
      <v-container fluid fill-height>
        <v-layout align-center justify-center>
          <v-flex xs12 sm8 md4>
          </v-flex>
        </v-layout>
      </v-container>
    </v-content>
  </v-app>
</template>

<script>
import classroomSwiper from "@/components/classroom/classroomSwiper.vue";
export default {
  name: "topPage",
  components: {
    classroomSwiper
  },
  data() {
    return {
    };
  },
};
</script>
