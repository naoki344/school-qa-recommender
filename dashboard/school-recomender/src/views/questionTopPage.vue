<template>
  <v-app id="inspire">
    <headerNav />
    <user-board />
    <questionList />
  </v-app>
</template>

<script>
import questionList from "@/components/question/questionList.vue";
import headerNav from "@/components/common/headerNav.vue";
import userBoard from "@/components/user/userBoard.vue";
export default {
  name: "TopPage",
  components: {
    headerNav,
    questionList,
    userBoard
  },
  data: () => ({})
};
</script>

