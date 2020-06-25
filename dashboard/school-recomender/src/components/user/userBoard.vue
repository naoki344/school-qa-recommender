<template>
  <v-container>
    <div class="all-info">
      <v-avatar
        size="110"
        class="avatar"
      >
        <v-icon v-if="myAvatarImageUrl == ''">
          mdi-account
        </v-icon>
        <v-img
          v-if="myAvatarImageUrl != ''"
          :src="myAvatarImageUrl"
          alt="Cropped Image"
        />
      </v-avatar>
      <div class="user-info">
        <h3 class="name">
          {{ nickname }}
          <span class="real-name">(本名:{{ fullName }})</span>
        </h3>
        <v-btn
          class="mt-2"
          depressed
          outlined
          @click="openUserModifyDialog"
        >
          プロフィールを編集
        </v-btn>
      </div>
    </div>
    <v-dialog
      v-model="userModifyDialog"
      scrollable
      width="450"
    >
      <userModify
        v-if="userModifyDialog"
        @close="closeUserModifyDialog"
      />
    </v-dialog>
  </v-container>
</template>

<script>
import { mapState } from "vuex";
import userModify from "@/components/user/userModify.vue";
export default {
  name: "UserBoard",
  components: {
    userModify
  },
  data() {
    return {
      userModifyDialog: false,
      myAvatarImageUrl: "",
      firstName: "",
      lastName: "",
      nickname: ""
    };
  },
  computed: {
    fullName() {
      return this.lastName + " " + this.firstName;
    },
    ...mapState({
      loginUser: state => state.user.loginUser.attributes
    })
  },
  mounted() {
    this.formInitialize();
    this.$store
      .dispatch("user/fetchMyAvatarImageUrl")
      .then(res => {
        console.log(res);
        this.myAvatarImageUrl = res;
      })
      .catch(() => {
        return "";
      });
  },
  methods: {
    openUserModifyDialog() {
      this.userModifyDialog = true;
    },
    formInitialize() {
      this.nickname = this.loginUser["nickname"];
      this.firstName = this.loginUser["custom:first_name"];
      this.lastName = this.loginUser["custom:last_name"];
    },
    closeUserModifyDialog() {
      this.userModifyDialog = false;
    }
  }
};
</script>

<style lang="scss" scoped>
.all-info {
  display: flex;
  justify-content: center;
  text-align: center;
  margin-top: 10px;
}
.avatar {
  display: inline-block;
  margin-right: 36px;
}
.real-name {
  font-size: 70%;
}
.user-info {
  margin: auto 0;
}
</style>