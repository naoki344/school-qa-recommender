<template>
  <v-app id="inspire">
    <headerNav />
    <classroomSwiper />
    <topDialog />
  </v-app>
</template>

<script>
import classroomSwiper from "@/components/classroom/classroomSwiper.vue";
import headerNav from "@/components/common/headerNav.vue";
import topDialog from "@/components/common/topDialog.vue";
export default {
  name: "topPage",
  props: {
    source: String
  },
  components: {
    classroomSwiper,
    headerNav,
    topDialog,
  },
  data: () => ({
  })
};
</script>
