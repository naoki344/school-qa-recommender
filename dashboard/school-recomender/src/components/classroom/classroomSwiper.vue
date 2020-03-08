<!-- The ref attr used to find the swiper instance -->
<template>
  <v-container>
    <swiper
      class="classroom-swiper-thumbs"
      :options="swiperOptionThumbs"
      ref="swiperThumbs"
    >
      <swiper-slide
        v-for="myClass in classroomList"
        :key="myClass.classroom.classroom_id"
        >{{ myClass.classroom.name }}</swiper-slide
      >
    </swiper>
    <swiper :options="swiperOptionTop" ref="swiperTop">
      <swiper-slide
        v-for="myClass in classroomList"
        :key="myClass.classroom.classroom_id"
      >
        <h1>{{ myClass.classroom.name }}</h1>
        <h2>{{ myClass.classmate.join_status }}</h2>

        <v-list two-line subheader>
          <v-subheader>新着</v-subheader>

          <v-list-item v-for="item in items" :key="item.title" link>
            <v-list-item-avatar>
              <v-icon :class="[item.iconClass]">{{ item.icon }}</v-icon>
            </v-list-item-avatar>

            <v-list-item-content>
              <v-list-item-title>{{ item.title }}</v-list-item-title>

              <v-list-item-subtitle>{{ item.subtitle }}</v-list-item-subtitle>
            </v-list-item-content>

            <v-list-item-action>
              <v-btn icon>
                <v-icon color="grey lighten-1">mdi-information</v-icon>
              </v-btn>
            </v-list-item-action>
          </v-list-item>

          <v-divider></v-divider>

          <v-subheader>履歴</v-subheader>

          <v-list-item v-for="item in items2" :key="item.title" link>
            <v-list-item-avatar>
              <v-icon :class="[item.iconClass]">{{ item.icon }}</v-icon>
            </v-list-item-avatar>

            <v-list-item-content>
              <v-list-item-title>{{ item.title }}</v-list-item-title>

              <v-list-item-subtitle>{{ item.subtitle }}</v-list-item-subtitle>
            </v-list-item-content>

            <v-list-item-action>
              <v-btn icon ripple>
                <v-icon color="grey lighten-1">mdi-information</v-icon>
              </v-btn>
            </v-list-item-action>
          </v-list-item>
        </v-list>
        <amplify-s3-image :imagePath="myClass.classroom.image_url"></amplify-s3-image>
      </swiper-slide>
      <!-- Optional controls -->
      <div class="swiper-pagination" slot="pagination"></div>
      <div class="swiper-button-prev" slot="button-prev"></div>
      <div class="swiper-button-next" slot="button-next"></div>
      <div class="swiper-scrollbar" slot="scrollbar"></div>
    </swiper>
    <v-btn color="green darken-1" @click="fetchS3Object">画像取得</v-btn>
    <v-col clos="2" md="3" lg="3">
      <v-file-input chips label="画像アップロード" accept="image/*" show-size v-model="file"></v-file-input>
      <v-btn color="green darken-1" @click="putS3PublicFile">アップロード</v-btn>
      <img :src="url">
    </v-col>
  </v-container>
</template>

<script>
import { mapState } from "vuex";
import "swiper/dist/css/swiper.css";
import { swiper, swiperSlide } from "vue-awesome-swiper";
import { components } from 'aws-amplify-vue';

export default {
  name: "classroomSwiper",
  components: {
    swiper,
    swiperSlide,
    ...components
  },
  data() {
    return {
      file: null,
      url: "",
      imagePath: 'fireworks001.jpg',
      swiperOptionTop: {
        spaceBetween: 10,
        navigation: {
          nextEl: ".swiper-button-next",
          prevEl: ".swiper-button-prev"
        }
      },
      swiperOptionThumbs: {
        spaceBetween: 20,
        centeredSlides: true,
        slidesPerView: "auto",
        touchRatio: 0.2,
        slideToClickedSlide: true,
        watchSlidesVisibility: true,
        watchSlidesProgress: true
      },
      items: [
        {
          icon: "folder",
          iconClass: "grey lighten-1 white--text",
          title: "Photos",
          subtitle: "Jan 9, 2014"
        },
        {
          icon: "folder",
          iconClass: "blue white--text",
          title: "Recipes",
          subtitle: "Jan 17, 2014"
        },
        {
          icon: "folder",
          iconClass: "grey lighten-1 white--text",
          title: "Work",
          subtitle: "Jan 28, 2014"
        }
      ],
      items2: [
        {
          icon: "assignment",
          iconClass: "blue white--text",
          title: "Vacation itinerary",
          subtitle: "Jan 20, 2014"
        },
        {
          icon: "call_to_action",
          iconClass: "amber white--text",
          title: "Kitchen remodel",
          subtitle: "Jan 10, 2014"
        }
      ]
    };
  },
  computed: {
    ...mapState({
      classroomList: state => state.classroom.myClassroomList
    })
  },
  methods: {
    fetchClassroomList() {
      this.$store.dispatch("classroom/fetchMyClassroomList");
    },
    fetchS3Object(path) {
      this.$store.dispatch("getS3PublicFile", path)
        .then((url) => {
          this.url = url;
        })
        .catch(err => {
          console.log(err);
        });
    },
    putS3PublicFile() {
      console.log(this.file);
      let filePath = this.file.name;
      this.$store.dispatch("putS3PublicFile", {
        filePath: filePath,
        data: this.file,
        })
        .then((data) => {
          this.fetchS3Object(data.key);
        })
        .catch(err => {
          console.log(err);
        });
    }
  },
  mounted() {
    this.$nextTick(() => {
      const swiperTop = this.$refs.swiperTop.swiper;
      const swiperThumbs = this.$refs.swiperThumbs.swiper;
      swiperTop.controller.control = swiperThumbs;
      swiperThumbs.controller.control = swiperTop;
    });
    this.fetchClassroomList();
  }
};
</script>

<style lang="scss" scoped>
.classroom-swiper-thumbs {
  .swiper-slide {
    width: auto;
    padding: 0 10px;
  }
  .swiper-slide-active {
    border-bottom: 2px solid rgb(9, 8, 53);
    color: rgb(9, 8, 53) !important;
    font-weight: bold;
  }
}
</style>