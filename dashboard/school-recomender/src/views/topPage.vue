<template>
  <v-app>
    <v-content>
      <v-container fluid fill-height>
        <v-layout align-center justify-center>
          <v-flex xs12 sm8 md4>
            <v-btn-toggle v-model="text" mandatory tile borderless color="black">
              <v-btn value="student" :color="isStudent() ? 'yellow' : ''" flat>生徒</v-btn>
              <v-btn value="teacher" :color="!isStudent() ? 'yellow' : ''" flat>先生</v-btn>
            </v-btn-toggle>
          </v-flex>
        </v-layout>
      </v-container>
    </v-content>
  </v-app>
</template>

<script>
export default {
  name: "topPage",
  data() {
    return {
      text: "student"
    };
  },
  methods: {
    isStudent() {
      return this.text === "student";
    }
  },
  components: {}
};
</script>
