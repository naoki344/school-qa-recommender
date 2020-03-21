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
    <v-card-text>
      <v-form>
        <v-text-field
          v-model="email"
          prepend-icon="mdi-email"
          counter="25"
          hint="メールアドレスを入力"
          label="Email"
          required
        />
        <v-text-field
          v-model="emailConfirm"
          prepend-icon="mdi-email"
          counter="25"
          label="Email(確認)"
          required
        />
        <v-text-field
          v-model="nickname"
          prepend-icon
          counter="10"
          label="ニックネーム(表示名)"
          required
        />
        <v-row>
          <v-col>
            <v-text-field
              v-model="lastName"
              prepend-icon
              counter="10"
              label="姓"
              required
            />
          </v-col>
          <v-col>
            <v-text-field
              v-model="firstName"
              prepend-icon
              counter="10"
              label="名"
              required
            />
          </v-col>
        </v-row>
        <v-row>
          <v-col>
            <v-text-field
              v-model="lastNameKana"
              prepend-icon
              counter="10"
              label="姓(カナ)"
              required
            />
          </v-col>
          <v-col>
            <v-text-field
              v-model="firstNameKana"
              prepend-icon
              counter="10"
              label="名(カナ)"
              required
            />
          </v-col>
        </v-row>
        <v-text-field
          v-model="password"
          :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
          :type="showPassword ? 'text' : 'password'"
          name="input-10-1"
          prepend-icon="mdi-key"
          label="パスワード"
          counter
          required
          @click:append="showPassword = !showPassword"
        />
        <v-text-field
          v-model="passwordConfirm"
          :append-icon="showPasswordConfirm ? 'mdi-eye' : 'mdi-eye-off'"
          :type="showPasswordConfirm ? 'text' : 'password'"
          name="input-10-1"
          prepend-icon="mdi-key"
          label="パスワード(確認)"
          counter
          required
          @click:append="showPasswordConfirm = !showPasswordConfirm"
        />

        <v-checkbox
          v-model="checkbox"
          :rules="[v => !!v || 'You must agree to continue!']"
          label="同意しますか?"
          required
        />
      </v-form>
    </v-card-text>
    <v-card-actions>
      <v-spacer />
      <v-btn
        color="yellow darken-1"
        block
        @click="userSignUp"
      >
        登録
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
import "@mdi/font/css/materialdesignicons.css";
export default {
  name: "UserSignUp",
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
    showPasswordConfirm: false
  }),
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
          console.log(err);
        });
    }
  }
};
</script>
