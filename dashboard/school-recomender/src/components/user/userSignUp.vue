<template>
  <v-card
    class="elevation-6"
    height="100%"
    width="100%"
  >
    <v-toolbar
      color="yellow darken-1"
      flat
    >
      <v-spacer />
      <v-toolbar-title>
        <strong>アカウント作成</strong>
      </v-toolbar-title>
      <v-spacer />
    </v-toolbar>
    <p>{{ errorMessage }}</p>
    <avatarCreate />
    <v-card-text>
      <v-form
        ref="form"
        @input="validation()"
      >
        <v-text-field
          v-model="nickname"
          class="user-register-input-form"
          autofocus
          prepend-icon
          counter="10"
          label="ニックネーム(表示名)"
          :rules="[required]"
          required
          @keyup.prevent.enter="moveNext"
        />
        <v-row>
          <v-col>
            <v-text-field
              v-model="lastName"
              class="user-register-input-form"
              prepend-icon
              counter="10"
              label="姓"
              :rules="[required]"
              required
              @keyup.prevent.enter="moveNext"
            />
          </v-col>
          <v-col>
            <v-text-field
              v-model="firstName"
              class="user-register-input-form"
              prepend-icon
              counter="10"
              required
              label="名"
              :rules="[required]"
              @keyup.prevent.enter="moveNext"
            />
          </v-col>
        </v-row>
        <v-row>
          <v-col>
            <v-text-field
              v-model="lastNameKana"
              class="user-register-input-form"
              prepend-icon
              counter="10"
              label="姓(カナ)"
              :rules="[required]"
              required
              @keyup.prevent.enter="moveNext"
            />
          </v-col>
          <v-col>
            <v-text-field
              v-model="firstNameKana"
              class="user-register-input-form"
              prepend-icon
              counter="10"
              label="名(カナ)"
              :rules="[required]"
              required
              @keyup.prevent.enter="moveNext"
            />
          </v-col>
        </v-row>
        <v-text-field
          v-model="email"
          class="user-register-input-form"
          prepend-icon="mdi-email"
          hint="メールアドレスを入力"
          label="Email"
          :rules="[required]"
          @keyup.prevent.enter="moveNext"
        />
        <v-text-field
          v-model="emailConfirm"
          class="user-register-input-form"
          prepend-icon="mdi-email"
          label="Email(確認)"
          :rules="[required, v => v === email || 'メールアドレスが一致していません',]"
          @keyup.prevent.enter="moveNext"
        />
        <v-text-field
          v-model="password"
          class="user-register-input-form"
          :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
          :type="showPassword ? 'text' : 'password'"
          name="input-10-1"
          prepend-icon="mdi-key"
          label="パスワード"
          :rules="[required]"
          counter
          required
          @keyup.prevent.enter="moveNext"
          @click:append="showPassword = !showPassword"
        />
        <v-text-field
          v-model="passwordConfirm"
          class="user-register-input-form"
          :append-icon="showPasswordConfirm ? 'mdi-eye' : 'mdi-eye-off'"
          :type="showPasswordConfirm ? 'text' : 'password'"
          :rules="[required, v => v === password || 'パスワードが一致していません',]"
          name="input-10-1"
          prepend-icon="mdi-key"
          label="パスワード(確認)"
          counter
          @click:append="showPasswordConfirm = !showPasswordConfirm"
        />
        <v-checkbox
          v-model="checkbox"
          :rules="[v => !!v || '登録には同意が必要です']"
          label="同意しますか?"
        />
      </v-form>
    </v-card-text>
    <v-card-actions>
      <v-spacer />
      <v-btn
        color="yellow darken-1"
        class="user-register-input-form"
        block
        :disabled="!buttonActive"
        @click="userSignUp"
      >
        登録
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
import avatarCreate from "@/components/avatar/avatarCreate.vue";
import "@mdi/font/css/materialdesignicons.css";
export default {
  name: "UserSignUp",
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
