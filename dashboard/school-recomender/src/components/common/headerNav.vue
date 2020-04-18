<template>
  <v-container>
    <v-navigation-drawer
      v-model="drawer"
      :clipped="$vuetify.breakpoint.lgAndUp"
      app
      fixed
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
            append-icon=""
          >
            <template v-slot:activator>
              <v-list-item-content>
                <v-list-item-title>
                  {{ item.text }}
                </v-list-item-title>
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
                <v-list-item-title>
                  {{ child.text }}
                </v-list-item-title>
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
              <v-list-item-title>
                {{ item.text }}
              </v-list-item-title>
            </v-list-item-content>
          </v-list-item>
        </template>
      </v-list>
    </v-navigation-drawer>
    <v-app-bar
      :clipped-left="$vuetify.breakpoint.lgAndUp"
      app
      color="yellow darken-1"
    >
      <v-app-bar-nav-icon @click.stop="drawer = !drawer" />
      <v-toolbar-title style="width: 100%; display: flex; padding: 0; justify-content: center;">
        <img src="@/assets/toi-toy-logo-wide-s--no-border-small.png">
      </v-toolbar-title>
      <v-avatar
        size="40"
      >
        <v-icon
          v-if="myAvatarImageUrl == ''"
        >
          mdi-account
        </v-icon>
        <v-img
          v-if="myAvatarImageUrl != ''"
          :src="myAvatarImageUrl"
          alt="Cropped Image"
        />
      </v-avatar>
    </v-app-bar>
  </v-container>
</template>

<script>
export default {
  name: "HeaderNav",
  data: () => ({
    drawer: null,
    items: [
      { link: "/", icon: "mdi-desktop-mac", text: "マイページ" },
      {
        link: "/questionTop",
        icon: "mdi-account-question",
        text: "トイ（TOI）"
      },
      { link: "/userLogout", icon: "mdi-logout", text: "ログアウト" }
    ],
    myAvatarImageUrl: "",
  }),
  mounted() {
    this.$store.dispatch("user/fetchMyAvatarImageUrl")
      .then((res) => {
          console.log(res);
		  this.myAvatarImageUrl = res;
      })
      .catch(() => {
          return "";
      });
  }
};
</script>
