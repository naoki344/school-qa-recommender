<template>
  <v-container>
    <v-row>
      <v-col> </v-col>
    </v-row>
  </v-container>
</template>

<script>
import "@mdi/font/css/materialdesignicons.css";
export default {
  name: "student",
  data: () => ({
    classroomName: "",
    classroomExplain: "",
    classroomTag: "",
    classroomMemberCapacity: ""
  }),
  computed: {},
  methods: {
    classroomCreate() {
      this.$store
        .dispatch("classroomCreate", {
          classroomName: this.classroomName,
          classroomExplain: this.classroomExplain,
          classroomTag: this.classroomTag,
          checkbox: this.checkbox,
          classroomMemberCapacity: this.classroomMemberCapacity
        })
        .then(() => {
          this.$router.push({ path: "/userConfirm" });
        })
        .catch(err => {
          console.log(err);
        });
    }
  },
  filters: {}
};
</script>
