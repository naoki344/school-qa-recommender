<template>
  <v-app id="inspire">
    <headerNav />
    <questionList />
    <topDialog />
  </v-app>
</template>

<script>
import questionList from "@/components/question/questionList.vue";
import topDialog from "@/components/common/topDialog.vue";
import headerNav from "@/components/common/headerNav.vue";
export default {
  name: "topPage",
  props: {
    source: String
  },
  components: {
    headerNav,
    questionList,
    topDialog,
  },
  data: () => ({
  })
};
</script>

