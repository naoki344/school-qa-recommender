<template>
  <v-container class="pa-0">
    <div
      class="v-work-comment-mode-input"
    >
      <textarea id="work-comment-input-form" />
    </div>
  </v-container>
</template>

<script>
export default {
  name: "WorkCommentInputForm",
  mounted() {
    document.getElementById("work-comment-input-form").focus();
  },
}
</script>

<style lang="scss" scoped>
.v-work-comment-mode-input {
  position: fixed;
  top: 0;
  right: 0;
  bottom: 0;
  left: 0;
  padding: 20px 10px 0;
  background: rgba(0, 0, 0, 0.25);
  textarea {
    max-width: 100vw;
    width: calc(100vw - 20px);
    height: calc(100vh - 40px);
    background: rgba(255, 255, 255, 0.9);
  }
}
</style>
