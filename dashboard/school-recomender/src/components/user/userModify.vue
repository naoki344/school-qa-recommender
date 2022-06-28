<template>
  <v-card class="pa-0">
    <v-card-actions>
      <v-btn @click="closeDialog">
        戻る
      </v-btn>
      <v-spacer />
      <h2 class="card-title">
        プロフィールを編集
      </h2>
      <v-spacer />
      <v-btn
        color="yellow darken-1"
        class="user-register-input-form"
        :disabled="!inputFormIsValid"
        @click="userSignUp"
      >
        保存
      </v-btn>
    </v-card-actions>
    <v-divider />
    <v-card-text>
      <v-container class="pa-5">
        <p>{{ errorMessage }}</p>
        <avatarCreate
          :croped-image-url="avatarImageDataUrl"
          @changeCropedImage="changeAvatorImage"
        />
        <v-form
          ref="form"
          v-model="inputFormIsValid"
        >
          <v-text-field
            v-model="nickname"
            dense
            outlined
            class="user-register-input-form"
            prepend-icon
            counter="10"
            label="ニックネーム(表示名)"
            :rules="[rules.required]"
            required
            @keydown.prevent.enter="moveNext"
          />
          <v-row>
            <v-col>
              <v-text-field
                v-model="lastName"
                dense
                outlined
                class="user-register-input-form"
                prepend-icon
                counter="10"
                label="姓"
                :rules="[rules.required]"
                required
                @keydown.prevent.enter="moveNext"
              />
            </v-col>
            <v-col>
              <v-text-field
                v-model="firstName"
                dense
                outlined
                class="user-register-input-form"
                prepend-icon
                counter="10"
                required
                label="名"
                :rules="[rules.required]"
                @keydown.prevent.enter="moveNext"
              />
            </v-col>
          </v-row>
        </v-form>
      </v-container>
    </v-card-text>
  </v-card>
</template>

<script>
import { mapState } from "vuex";
import avatarCreate from "@/components/avatar/avatarCreate.vue";
import "@mdi/font/css/materialdesignicons.css";
export default {
  name: "UserModify",
  components: {
    avatarCreate
  },
  data() {
    return {
      nickname: "",
      lastName: "",
      firstName: "",
      rules: {
        required: value => !!value || "入力されていません"
      },
      errorMessage: "",
      avatarImageDataUrl: "",
      inputFormIsValid: false
    };
  },
  computed: {
    elements() {
      return [...document.getElementsByClassName("user-register-input-form")];
    },
    originPagePath() {
      return this.$route.query.originPagePath;
    },
    ...mapState({
      loginUser: state => state.user.loginUser.attributes
    })
  },
  mounted() {
    this.formInitialize();
  },
  methods: {
    formInitialize() {
      this.nickname = this.loginUser["nickname"];
      this.firstName = this.loginUser["custom:first_name"];
      this.lastName = this.loginUser["custom:last_name"];
      this.avatarImageDataUrl = this.loginUser["custom:avatar_url"];
    },
    userSignUp() {
      this.inputFormIsValid = this.$refs.form.validate();
      if (this.inputFormIsValid === false) return;
      this.$store
        .dispatch("user/userSignUp", {
          nickname: this.nickname,
          firstName: this.firstName,
          lastName: this.lastName,
          username: this.username,
          avatarImageDataUrl: this.avatarImageDataUrl
        })
        .then(() => {
          if (this.originPagePath == undefined || this.originPagePath == null) {
            this.$router.push({
              path: "/userVerify",
              query: { email: this.email }
            });
          } else {
            this.$router.push({
              path: "/userVerify",
              query: { email: this.email, originPagePath: this.originPagePath }
            });
          }
        })
        .catch(err => {
          console.log(err);
          this.errorMessage = err.message;
        });
    },
    findIndex(target) {
      return this.elements.findIndex(
        e => e.getElementsByTagName("input")[0] === target
      );
    },
    moveFocus(index) {
      if (this.elements[index]) {
        this.elements[index].getElementsByTagName("input")[0].focus();
      }
    },
    moveNext(event) {
      if (event.keyCode !== 13) {
        return;
      }
      const index = this.findIndex(event.target);
      this.moveFocus(index + 1);
    },
    changeAvatorImage(data) {
      this.avatarImageDataUrl = data;
      console.log(this.avatarImageDataUrl);
    },
    closeDialog() {
      this.$emit("close");
    }
  }
};
</script>

<style lang="scss">
@media screen and (max-width: 600px) {
  .card-title {
    font-size: 100%;
  }
}
</style>