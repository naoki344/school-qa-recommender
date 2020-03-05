<template>
  <div class="home">
    <QuestionIndex />
  </div>
</template>

<script>
// @ is an alias to /src
import QuestionIndex from "@/components/QuestionIndex.vue";

export default {
  name: "Home",
  components: {
    QuestionIndex
  }
};
</script>
