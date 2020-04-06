<template>
  <v-app id="inspire">
    <headerNav />
    <questionList />
  </v-app>
</template>

<script>
import questionList from "@/components/question/questionList.vue";
import headerNav from "@/components/common/headerNav.vue";
export default {
  name: "TopPage",
  components: {
    headerNav,
    questionList,
  },
  data: () => ({
  })
};
</script>

