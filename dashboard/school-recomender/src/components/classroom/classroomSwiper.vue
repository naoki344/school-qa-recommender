<!-- The ref attr used to find the swiper instance -->
<template>
  <v-content>
    <swiper
      class="classroom-swiper-thumbs"
      :options="swiperOptionThumbs"
      ref="swiperThumbs"
    >
      <swiper-slide
        v-for="myClass in classroomList"
        :key="myClass.classroom.classroom_id"
      >{{ myClass.classroom.name }}</swiper-slide>
    </swiper>
    <swiper :options="swiperOptionTop" ref="swiperTop">
      <swiper-slide v-for="myClass in classroomList" :key="myClass.classroom.classroom_id">
        <h1>{{ myClass.classroom.name }}</h1>
        <h2>{{ myClass.classmate.join_status }}</h2>
        <v-list two-line subheader>
          <v-subheader>新着</v-subheader>

          <v-list-item v-for="item in items" :key="item.title" link @click="dialog = !dialog">
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
        <!--amplify-s3-image :imagePath="myClass.classroom.image_url"></amplify-s3-image-->
      </swiper-slide>
      <!-- Optional controls -->
      <div class="swiper-pagination" slot="pagination"></div>
      <div class="swiper-button-prev" slot="button-prev"></div>
      <div class="swiper-button-next" slot="button-next"></div>
      <div class="swiper-scrollbar" slot="scrollbar"></div>
    </swiper>
    <v-dialog v-model="dialog" persistent scrollable width="800px">
      <v-card>
        <v-card-title class="yellow darken-1">
          <v-spacer />
          <strong>解答作成</strong>
          <v-spacer />
        </v-card-title>
        <v-divider></v-divider>
        <v-carousel cycle height="400" hide-delimiter-background show-arrows-on-hover>
          <v-carousel-item v-for="(slide, i) in slides" :key="i">
            <v-sheet :color="colors[i]" height="100%">
              <v-row class="fill-height" align="center" justify="center">
                <div class="display-3">{{ slide }} Slide</div>
              </v-row>
            </v-sheet>
          </v-carousel-item>
        </v-carousel>
        <v-card-text>
          <v-container>
            <v-row class="mx-2">
              <v-col class="align-center justify-space-between" cols="12">
                <v-row align="center" class="mr-0">
                  <v-avatar size="40px" class="mx-3">
                    <img src="//ssl.gstatic.com/s2/oz/images/sge/grey_silhouette.png" alt />
                  </v-avatar>
                  <v-text-field placeholder="Name" />
                </v-row>
              </v-col>
              <v-col cols="6">
                <v-text-field
                  prepend-icon="mdi-account-card-details-outline"
                  placeholder="Company"
                />
              </v-col>
              <v-col cols="6">
                <v-text-field placeholder="Job title" />
              </v-col>
              <v-col cols="12">
                <v-text-field prepend-icon="mdi-mail" placeholder="Email" />
              </v-col>
              <v-col cols="12">
                <v-text-field prepend-icon="mdi-text" placeholder="Notes" />
              </v-col>
              <v-col cols="12">
                <v-text-field prepend-icon="mdi-text" placeholder="Notes" />
              </v-col>
              <v-col cols="12">
                <v-text-field prepend-icon="mdi-text" placeholder="Notes" />
              </v-col>
              <v-col cols="12">
                <v-text-field prepend-icon="mdi-text" placeholder="Notes" />
              </v-col>
            </v-row>
          </v-container>
        </v-card-text>
        <v-divider></v-divider>

        <v-card-actions>
          <v-spacer />
          <v-btn text color="primary" @click="dialog = false">キャンセル</v-btn>
          <v-btn text @click="dialog = false">送信</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-content>
</template>

<script>
import { mapState } from "vuex";
import "swiper/dist/css/swiper.css";
import { swiper, swiperSlide } from "vue-awesome-swiper";
import { components } from "aws-amplify-vue";

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
      imagePath: "fireworks001.jpg",
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
      dialog: false,
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
      ],
      colors: ["indigo", "warning", "pink darken-2"],
      slides: ["First", "Second", "Third"]
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
      this.$store
        .dispatch("getS3PublicFile", path)
        .then(url => {
          this.url = url;
        })
        .catch(err => {
          console.log(err);
        });
    },
    putS3PublicFile() {
      console.log(this.file);
      let filePath = this.file.name;
      this.$store
        .dispatch("putS3PublicFile", {
          filePath: filePath,
          data: this.file
        })
        .then(data => {
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
