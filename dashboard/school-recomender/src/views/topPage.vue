<template>
  <v-app id="inspire">
    <headerNav />
    <classroomSwiper />
  </v-app>
</template>

<script>
import classroomSwiper from "@/components/classroom/classroomSwiper.vue";
import headerNav from "@/components/common/headerNav.vue";
export default {
  name: "topPage",
  props: {
    source: String
  },
  components: {
    headerNav,
    classroomSwiper,
  },
  data: () => ({
  })
};
</script>
