<template>
  <div>
    <v-navigation-drawer
      v-model="drawer"
      clipped
      app
    >
      <v-list dense>
        <template v-for="item in items">
          <v-row
            v-if="item.heading"
            :key="item.heading"
            align="center"
          >
            <v-col cols="6">
              <v-subheader v-if="item.heading">
                {{ item.heading }}
              </v-subheader>
            </v-col>
            <v-col
              cols="6"
              class="text-center"
            >
              <a
                href="#!"
                class="body-2 black--text"
              >EDIT</a>
            </v-col>
          </v-row>
          <v-list-group
            v-else-if="item.children"
            :key="item.text"
            v-model="item.model"
            :prepend-icon="item.model ? item.icon : item['icon-alt']"
            append-icon
          >
            <template v-slot:activator>
              <v-list-item-content>
                <v-list-item-title>{{ item.text }}</v-list-item-title>
              </v-list-item-content>
            </template>
            <v-list-item
              v-for="(child, i) in item.children"
              :key="i"
              link
            >
              <v-list-item-action v-if="child.icon">
                <v-icon>{{ child.icon }}</v-icon>
              </v-list-item-action>
              <v-list-item-content>
                <v-list-item-title>{{ child.text }}</v-list-item-title>
              </v-list-item-content>
            </v-list-item>
          </v-list-group>
          <v-list-item
            v-else
            :key="item.text"
            link
            :to="item.link"
          >
            <v-list-item-action>
              <v-icon>{{ item.icon }}</v-icon>
            </v-list-item-action>
            <v-list-item-content>
              <v-list-item-title>{{ item.text }}</v-list-item-title>
            </v-list-item-content>
          </v-list-item>
        </template>
        <v-list-item @click="logoutDialog = true">
          <v-list-item-action>
            <v-icon>{{ logoutItem.icon }}</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>{{ logoutItem.text }}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>
    <v-app-bar
      clipped-left
      app
      color="yellow darken-1"
    >
      <v-app-bar-nav-icon @click.stop="drawer = !drawer" />
      <v-toolbar-title style="width: 100%; display: flex; padding: 0; justify-content: center;">
        <img
          src="@/assets/toi-toy-logo-wide-s--no-border-small.png"
          style="cursor: pointer;"
          @click="goToTopPage"
        >
      </v-toolbar-title>
      <v-btn
        fab
        depressed
        color="yellow darken-1"
        @click="goToQuestionTop"
      >
        <v-avatar size="34">
          <v-icon v-if="myAvatarImageUrl == ''">
            mdi-account
          </v-icon>
          <v-img
            v-if="myAvatarImageUrl != ''"
            :src="myAvatarImageUrl"
            alt="Cropped Image"
          />
        </v-avatar>
      </v-btn>
    </v-app-bar>
    <v-dialog
      v-model="logoutDialog"
      width="300px"
    >
      <v-card style="texta">
        <v-card-title>
          <v-spacer />
          <v-img
            max-width="180px"
            src="@/assets/toi-toy-logo-wide-s--no-border-small.png"
          />
          <v-spacer />
        </v-card-title>
        <v-card-text class="px-3 py-4">
          <p style="text-align: center;">
            <strong>Toi-Toy からログアウトしますか？</strong>
          </p>
        </v-card-text>
        <v-card-actions class="justify-space-around">
          <v-btn @click="logoutDialog = false">
            キャンセル
          </v-btn>
          <v-btn
            color="yellow darken-1"
            @click="logout"
          >
            ログアウト
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

  <script>
export default {
  name: "HeaderNav",
  components: {},
  data: () => ({
    drawer: null,
    logoutDialog: false,
    items: [
      { link: "/", icon: "mdi-desktop-mac", text: "マイページ" },
      {
        link: "/questionTop",
        icon: "mdi-account-question",
        text: "トイ（TOI）"
      }
    ],
    logoutItem: { icon: "mdi-logout", text: "ログアウト" },
    myAvatarImageUrl: ""
  }),
  mounted() {
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
    logout() {
      this.$router.push({ path: "/userLogout" });
    },
    goToTopPage() {
      this.$router.push({ path: "/" });
    },
    goToQuestionTop() {
      this.$router.push({ path: "/questionTop" });
    }
  }
};
</script>
