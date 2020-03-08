<template>
  <v-app id="inspire">
    <classroomSwiper />
    <topDialog />
  </v-app>
</template>

<script>
import classroomSwiper from "@/components/classroom/classroomSwiper.vue";
import topDialog from "@/components/common/topDialog.vue";
export default {
  name: "topPage",
  props: {
    source: String
  },
  components: {
    classroomSwiper,
    topDialog,
  },
  data: () => ({
  })
};
</script>
