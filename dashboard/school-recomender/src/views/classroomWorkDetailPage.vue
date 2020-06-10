<!-- The ref attr used to find the swiper instance -->
<template>
  <v-app>
    <v-app-bar
      fixed
      color="yellow darken-1"
      style="max-height: 56px;"
    >
      <v-btn
        icon
        @click="$router.go(-1)"
      >
        <v-icon>mdi-close</v-icon>
      </v-btn>
      <v-toolbar-title>{{ classroomName }}</v-toolbar-title>
      <v-spacer />
      <v-btn icon>
        <v-icon>mdi-reload</v-icon>
      </v-btn>
    </v-app-bar>

    <v-content class="pt-12">
      <workDetail
        v-if="workExisted"
        :work-id="workId"
        :classroom-id="classroomId"
        :question="question"
        :work="work"
      />
    </v-content>
  </v-app>
</template>

<script>
import workDetail from "@/components/work/workDetail.vue";

export default {
  name: "ClassroomWorkDetailPage",
  components: {
    workDetail
  },
  data: () => ({
    work: null,
    question: null,
    workId: null,
    classroomId: null,
    workExisted: false,
    classroomName: ""
  }),
  async created() {
    this.workId = Number(this.$route.query.work_id);
    this.classroomId = Number(this.$route.query.classroom_id);
    this.classroom = this.$store
      .dispatch("classroom/fetchClassroom", this.classroomId)
      .then(data => {
        this.classroomName = data.name;
      })
      .catch(err => {
        console.log(err);
      });
    await this.findClassroomWork();
  },
  methods: {
    findClassroomWork() {
      console.log(this.workId);
      console.log(this.classroomId);
      if (this.workId == null) return;
      if (this.classroomId == null) return;
      const params = {
        classroomId: this.classroomId,
        workId: this.workId
      };
      this.$store
        .dispatch("classroom/fetchClassroomWork", params)
        .then(data => {
          this.work = data["work"];
          this.question = data["question"];
          this.workExisted = true;
        })
        .catch(err => {
          console.log(err);
        });
    }
  }
};
</script>
