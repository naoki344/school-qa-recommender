<template>
  <v-card class="elevation-6" height="100%" width="100%">
    <v-toolbar color="yellow darken-1" flat>
      <v-spacer></v-spacer>
      <v-toolbar-title>
        <strong>アカウント作成</strong>
      </v-toolbar-title>
      <v-spacer></v-spacer>
    </v-toolbar>
    <p>{{errorMessage}}</p>
    <avatarCreate />
    <v-card-text>
      <v-form @input="validation()" ref="form">
        <v-text-field
          @keyup.prevent.enter="moveNext"
          class="user-register-input-form"
          v-model="nickname"
          autofocus
          prepend-icon
          counter="10"
          label="ニックネーム(表示名)"
          :rules="[required]"
        ></v-text-field>
        <v-row>
          <v-col>
            <v-text-field
              @keyup.prevent.enter="moveNext"
              v-model="lastName"
              class="user-register-input-form"
              prepend-icon
              counter="10"
              label="姓"
              :rules="[required]"
            ></v-text-field>
          </v-col>
          <v-col>
            <v-text-field
              v-model="firstName"
              @keyup.prevent.enter="moveNext"
              class="user-register-input-form"
              prepend-icon
              counter="10"
              label="名"
              :rules="[required]"
            ></v-text-field>
          </v-col>
        </v-row>
        <v-row>
          <v-col>
            <v-text-field
              v-model="lastNameKana"
              @keyup.prevent.enter="moveNext"
              class="user-register-input-form"
              prepend-icon
              counter="10"
              label="姓(カナ)"
              :rules="[required]"
            ></v-text-field>
          </v-col>
          <v-col>
            <v-text-field
              v-model="firstNameKana"
              @keyup.prevent.enter="moveNext"
              class="user-register-input-form"
              prepend-icon
              counter="10"
              label="名(カナ)"
              :rules="[required]"
            ></v-text-field>
          </v-col>
        </v-row>
        <v-text-field
          v-model="email"
          @keyup.prevent.enter="moveNext"
          class="user-register-input-form"
          prepend-icon="mdi-email"
          hint="メールアドレスを入力"
          label="Email"
          :rules="[required]"
        ></v-text-field>
        <v-text-field
          v-model="emailConfirm"
          @keyup.prevent.enter="moveNext"
          class="user-register-input-form"
          prepend-icon="mdi-email"
          label="Email(確認)"
          :rules="[required,
          v => v === this.email || 'メールアドレスが一致していません',]"
        ></v-text-field>
        <v-text-field
          v-model="password"
          @keyup.prevent.enter="moveNext"
          class="user-register-input-form"
          :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
          :type="showPassword ? 'text' : 'password'"
          name="input-10-1"
          prepend-icon="mdi-key"
          label="パスワード"
          :rules="[required]"
          counter
          @click:append="showPassword = !showPassword"
        ></v-text-field>
        <v-text-field
          v-model="passwordConfirm"
          class="user-register-input-form"
          :append-icon="showPasswordConfirm ? 'mdi-eye' : 'mdi-eye-off'"
          :type="showPasswordConfirm ? 'text' : 'password'"
          :rules="[required,
          v => v === this.password || 'パスワードが一致していません',]"
          name="input-10-1"
          prepend-icon="mdi-key"
          label="パスワード(確認)"
          counter
          @click:append="showPasswordConfirm = !showPasswordConfirm"
        ></v-text-field>
        <v-checkbox v-model="checkbox" :rules="[v => !!v || '登録には同意が必要です']" label="同意しますか?"></v-checkbox>
      </v-form>
    </v-card-text>
    <v-card-actions>
      <v-spacer></v-spacer>
      <v-btn
        color="yellow darken-1"
        class="user-register-input-form"
        @click="userSignUp"
        block
        :disabled="!buttonActive"
      >登録</v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
import avatarCreate from "@/components/avatar/avatarCreate.vue";
import "@mdi/font/css/materialdesignicons.css";
export default {
  name: "userSignUp",
  components: {
    avatarCreate
  },
  data: () => ({
    email: "",
    emailConfirm: "",
    nickname: "",
    lastName: "",
    firstName: "",
    lastNameKana: "",
    firstNameKana: "",
    password: "",
    passwordConfirm: "",
    checkbox: false,
    showPassword: false,
    showPasswordConfirm: false,
    buttonActive: false,
    required: value => !!value || "入力されていません",
    errorMessage: ""
  }),
  computed: {
    elements() {
      return [...document.getElementsByClassName("user-register-input-form")];
    }
  },
  methods: {
    userSignUp() {
      this.$store
        .dispatch("user/userSignUp", {
          email: this.email,
          nickname: this.nickname,
          firstName: this.firstName,
          lastName: this.lastName,
          firstNameKana: this.firstNameKana,
          lastNameKana: this.lastNameKana,
          username: this.username,
          password: this.password
        })
        .then(() => {
          this.$router.push({ path: "/userConfirm" });
        })
        .catch(err => {
          this.errorMessage = err.message;
        });
    },
    validation() {
      this.buttonActive = this.$refs.form.validate();
      this.$refs.form.resetValidation();
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
      const index = this.findIndex(event.target);
      this.moveFocus(index + 1);
    }
  }
};
</script>