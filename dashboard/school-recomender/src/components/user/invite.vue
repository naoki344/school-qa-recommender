<template>
  <v-content class="pt-0">
    <v-container>
      <v-row
        justify="center"
        class="mb-12"
      >
        <v-img
          max-width="180px"
          src="@/assets/toi-toy-logo-wide-s--no-border-small.png"
        />
      </v-row>
      <v-row justify="center">
        <div>
          <h2>「{{ classroom.name }}」に参加する</h2>
          <p
            align="center"
            class="ma-0"
          >
            {{ classroom.caption }}
          </p>
        </div>
      </v-row>
      <v-row justify="center">
        <v-col cols="7">
          <div
            v-for="owner in classroom.owner_list"
            :key="owner.user_id"
            class="ma-1"
          >
            <v-avatar
              tile
              size="25"
              style="border-radius: 6px;"
            >
              <v-img :src="getUserAvatarImageUrl(owner.user_id)" />
            </v-avatar>
            <p class="font-weight-bold ma-2 owner-name">
              {{ owner.nickname }}
            </p>
          </div>
        </v-col>
      </v-row>
    </v-container>
    <v-btn
      block
      color="yellow darken-1"
      large
      @click="join"
    >
      <strong class="login">参加する</strong>
    </v-btn>
  </v-content>
</template>

<script>
export default {
  name: "Invite",
  data: () => ({
    classroom: {
      name: "英語クラス",
      caption: "英単語をメインに学ぶクラスです",
      owner_list: [
        {
          user_id: "79434f7e-b53f-4d3a-8c79-aedc7b73af39",
          nickname: "三好 直紀"
        },
        {
          user_id: "79434f7e-b53f-4d3a-8c79-aedc7b73af39",
          nickname: "濵砂 大輝大輝"
        }
      ]
    }
  }),
  methods: {
    join() {
      alert("クラスに参加しました");
    },
    getUserAvatarImageUrl(userId) {
      return this.$store.getters["user/userAvatarImageUrl"](userId);
    }
  }
};
</script>

<style lang="scss" scoped>
.owner-name {
  display: inline-block;
}
.login {
  font-size: 20px;
}
</style>