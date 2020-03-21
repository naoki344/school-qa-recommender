<!-- The ref attr used to find the swiper instance -->
<template>
  <v-content>
    <v-dialog v-model="dialogVisible" fullscreen hide-overlay scrollable transition="dialog-bottom-transition" >
      <v-card>
        <v-toolbar color="yellow darken-1" style="max-height: 56px;">
          <v-btn icon @click="closeDialog()">
            <v-icon>mdi-close</v-icon>
          </v-btn>
          <v-toolbar-title>test</v-toolbar-title>
          <v-spacer></v-spacer>
          <v-btn icon @click="closeDialog()">
            <v-icon>mdi-reload</v-icon>
          </v-btn>
        </v-toolbar>
        <v-divider></v-divider>
        <v-card-text>
          <v-container>
            <p>aa</p>
          </v-container>
        </v-card-text>
      </v-card>
    </v-dialog>
  </v-content>
</template>

<script>
import { mapState } from "vuex";
import "swiper/dist/css/swiper.css";

export default {
  name: "classroomWorkDetail",
  props: {
    dialogVisible: {
      type: Boolean
    },
    work: {
      type: Object
    }
  },
  data() {
    return {
    }
  },
  computed: {
    ...mapState({
      classroomList: state => state.classroom.myClassroomList,
    }),
  },
  methods: {
    closeDialog() {
      this.$emit('closeDialog');
    },
    getImageUrl(obj) {
      if (obj["image_url"] == null) { return false }
      const path = obj["image_url"];
      if (this.imageList[path] != null) { return true }
      this.$store.dispatch("getS3PublicFile", path)
        .then((url) => {
          this.$set(this.imageList, path, url);
        })
        .catch(() => {
          return false;
        });
      return true;
    },
  },
};
</script>

<style lang="scss" scoped>
</style>

