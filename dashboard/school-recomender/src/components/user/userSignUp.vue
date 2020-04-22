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
    <avatarCreate
      :croped-image-url="avatarImageDataUrl"
      @changeCropedImage="changeAvatorImage"
    />
    <v-card-text>
      <v-form
        ref="form"
        v-model="inputFormIsValid"
      >
        <v-text-field
          v-model="nickname"
          class="user-register-input-form"
          autofocus
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
        <v-row>
          <v-col>
            <v-text-field
              v-model="lastNameKana"
              class="user-register-input-form"
              prepend-icon
              name="last-name-kana"
              counter="10"
              label="姓(カナ)"
              :rules="[rules.required]"
              required
              @keydown.prevent.enter="moveNext"
            />
          </v-col>
          <v-col>
            <v-text-field
              v-model="firstNameKana"
              class="user-register-input-form"
              name="first-name-kana"
              prepend-icon
              counter="10"
              label="名(カナ)"
              :rules="[rules.required]"
              required
              @keydown.prevent.enter="moveNext"
            />
          </v-col>
        </v-row>
        <v-text-field
          v-model="email"
          class="user-register-input-form"
          name="email"
          prepend-icon="mdi-email"
          hint="メールアドレスを入力"
          label="Email"
          :rules="[rules.required, rules.email]"
          @change="emailValidation"
          @keydown.prevent.enter="moveNext"
        />
        <v-text-field
          ref="emailConfirm"
          v-model="emailConfirm"
          name="email-confirm"
          class="user-register-input-form"
          prepend-icon="mdi-email"
          label="Email(確認)"
          :rules="[rules.required, rules.email, v => v === email || 'メールアドレスが一致していません',]"
          @keydown.prevent.enter="moveNext"
        />
        <v-text-field
          v-model="password"
          class="user-register-input-form"
          :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
          :type="showPassword ? 'text' : 'password'"
          name="password"
          prepend-icon="mdi-key"
          label="パスワード"
          :rules="[rules.required, rules.password]"
          counter
          required
          @keydown.prevent.enter="moveNext"
          @click:append="showPassword = !showPassword"
          @change="passwordValidation"
        />
        <v-text-field
          ref="passwordConfirm"
          v-model="passwordConfirm"
          class="user-register-input-form"
          :append-icon="showPasswordConfirm ? 'mdi-eye' : 'mdi-eye-off'"
          :type="showPasswordConfirm ? 'text' : 'password'"
          :rules="[
            rules.required,
            rules.password,
            v => v === password || 'パスワードが一致していません'
          ]"
          name="password-confirm"
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
        :disabled="!inputFormIsValid"
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
    rules: {
      required: value => !!value || "入力されていません",
      email: value => /.+@.+\..+/.test(value) || 'メールアドレスの形式が正しくありません',
      password: value => /^(?=.*?[a-z])(?=.*?\d)(?=.*?[!-\/:-@[-`{-~])[!-~]{6,100}$/.test(value) || "パスワードには、大文字、小文字、記号を使用してください",
    },
    errorMessage: "",
    avatarImageDataUrl: "",
    inputFormIsValid: false,
  }),
  computed: {
    elements() {
      return [...document.getElementsByClassName("user-register-input-form")];
    }
  },
  methods: {
    userSignUp() {
      this.inputFormIsValid = this.$refs.form.validate();
      if (this.inputFormIsValid === false) return
      this.$store
        .dispatch("user/userSignUp", {
          email: this.email,
          nickname: this.nickname,
          firstName: this.firstName,
          lastName: this.lastName,
          firstNameKana: this.firstNameKana,
          lastNameKana: this.lastNameKana,
          username: this.username,
          password: this.password,
          avatarImageDataUrl: this.avatarImageDataUrl
        })
        .then(() => {
          this.$router.push({
            path: "/userVerify",
            query: { email: this.email }
          });
        })
        .catch(err => {
          console.log(err)
          this.errorMessage = err.message;
        });
    },
    passwordValidation() {
      if (this.$refs.form == null) return;
      this.$refs.passwordConfirm.validate();
    },
    emailValidation() {
      if (this.$refs.form == null) return;
      this.$refs.emailConfirm.validate();
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
    }
  }
};
</script>
