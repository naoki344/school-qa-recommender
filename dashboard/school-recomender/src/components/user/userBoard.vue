<template>
  <v-container>
    <div class="all-info">
      <v-avatar
        size="120"
        class="avatar"
      >
        <v-img v-if="userAvatar" />
        <v-img
          v-else
          src="@/assets/question-no-image.png"
        />
      </v-avatar>
      <div class>
        <p>ニックネーム</p>
        <p>本名</p>
        <v-btn
          depressed
          outlined
          @click="openUserModifyDialog"
        >
          プロフィールを編集
        </v-btn>
      </div>
    </div>
    <v-dialog v-model="userModifyDialog">
      <userModify />
    </v-dialog>
  </v-container>
</template>

<script>
import userModify from "@/components/user/userModify.vue";
export default {
  name: "UserBoard",
  components: {
    userModify
  },
  data() {
    return {
      userAvatar: "",
      userModifyDialog: false
    };
  },
  methods: {
    openUserModifyDialog() {
      this.userModifyDialog = true;
    }
  }
};
</script>

<style lang="scss" scoped>
.all-info {
  display: flex;
  text-align: center;
  justify-content: center;
  margin-top: 10px;
}
.avatar {
  display: inline-block;
  margin-right: 40px;
}
.user-info {
  display: inline-block;
}
</style>