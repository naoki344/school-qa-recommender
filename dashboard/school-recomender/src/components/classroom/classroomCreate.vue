<template>
  <v-content>
    <v-card class="elevation-6" height="100%" width="100%">
      <v-toolbar color="yellow darken-1" flat>
        <v-spacer></v-spacer>
        <v-toolbar-title>
          <strong>クラス作成</strong>
        </v-toolbar-title>
        <v-spacer></v-spacer>
      </v-toolbar>
      <v-card-text>
        <v-form>
          <v-text-field v-model="classroomName" counter="25" label="クラス名" required></v-text-field>
          <v-text-field v-model="classroomExplain" counter="25" label="クラス説明" required></v-text-field>
          <v-text-field v-model="classroomTag" counter="25" label="タグ" required></v-text-field>
          <v-checkbox v-model="counterEn" class="ma-0 mr-2 ml-1" label="定員を設ける"></v-checkbox>
          <v-text-field
            v-model.number="classroomMemberCapacity"
            :disabled="!counterEn"
            dense
            :rules="[v => !!v || 'You must agree to continue!']"
            label="定員"
            required
          ></v-text-field>

          <v-checkbox
            v-model="checkbox"
            :rules="[v => !!v || 'You must agree to continue!']"
            label="非公開にする"
            required
          ></v-checkbox>
        </v-form>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="yellow darken-1" @click="classroomCreate" block>作成</v-btn>
      </v-card-actions>
    </v-card>
  </v-content>
</template>

<script>
import "@mdi/font/css/materialdesignicons.css";
export default {
  name: "classroomCreate",
  data: () => ({
    classroomName: "",
    classroomExplain: "",
    classroomTag: "",
    counterEn: false,
    classroomMemberCapacity: "",
    checkbox: false
  }),
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
  }
};
</script>

