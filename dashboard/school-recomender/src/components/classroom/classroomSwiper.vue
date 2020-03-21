<!-- The ref attr used to find the swiper instance -->
<template>
  <v-content>
    <swiper
      ref="swiperThumbs"
      class="classroom-swiper-thumbs"
      :options="swiperOptionThumbs"
    >
      <swiper-slide
        v-for="myClass in classroomList"
        :key="myClass.classroom.classroom_id"
      >
        {{ myClass.classroom.name }}
      </swiper-slide>
    </swiper>
    <swiper
      ref="swiperTop"
      :options="swiperOptionTop"
      class="py-2 px-0"
    >
      <swiper-slide
        v-for="myClass in classroomList"
        :key="myClass.classroom.classroom_id"
        style="text-align: left;"
      >
        <v-img
          v-if="getImageUrl(myClass.classroom)"
          class="mb-2"
          :src="imageList[myClass.classroom.image_url]"
          style="width: 100%; max-width: 760px; height: 150px; margin: auto;"
        />
        <div v-if="isShowClassroomContent(myClass)">
          <h1 class="pa-2">
            {{ myClass.classroom.name }}
          </h1>
          <v-list
            two-line
            subheader
          >
            <v-subheader>ワーク一覧</v-subheader>
            <v-list-item
              v-for="item in classroomWorkList[myClass.classroom.classroom_id]"
              :key="item.work_id"
              link
              @click="openWorkDetail(item)"
            >
              <!--v-list-item-avatar>
                <v-icon :class="[item.iconClass]">mdi-head-question</v-icon>
              </v-list-item-avatar-->
              <v-list-item-content>
                <v-list-item-title>{{ item.title }}</v-list-item-title>
                <v-list-item-subtitle>{{ item.caption }}</v-list-item-subtitle>
              </v-list-item-content>
              <v-btn icon>
                <v-icon color="grey lighten-1">
                  mdi-message
                </v-icon>
              </v-btn>
            </v-list-item>
            <v-divider />
          </v-list>
          <classroom-work-detail-dialog
            :work="selectedWork"
            :dialog-visible="workDialogVisible"
            @closeDialog="closeWorkDetailDialog()"
          />
        </div>
      </swiper-slide>
      <!-- Optional controls -->
      <div
        slot="pagination"
        class="swiper-pagination"
      />
      <div
        slot="button-prev"
        class="swiper-button-prev"
      />
      <div
        slot="button-next"
        class="swiper-button-next"
      />
      <div
        slot="scrollbar"
        class="swiper-scrollbar"
      />
    </swiper>
  </v-content>
</template>

<script>
import { mapState } from "vuex";
import "swiper/dist/css/swiper.css";
import { swiper, swiperSlide } from "vue-awesome-swiper";
import { components } from "aws-amplify-vue";
import classroomWorkDetailDialog from "@/components/classroom/classroomWorkDetailDialog.vue";

export default {
  name: "ClassroomSwiper",
  components: {
    swiper,
    swiperSlide,
    classroomWorkDetailDialog,
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
      imageList: [],
      selectedWork: {},
      swiperOptionThumbs: {
        spaceBetween: 20,
        centeredSlides: true,
        slidesPerView: "auto",
        touchRatio: 0.2,
        slideToClickedSlide: true,
        watchSlidesVisibility: true,
        watchSlidesProgress: true
      },
      workDialogVisible: false,
    };
  },
  computed: {
    ...mapState({
      classroomList: state => state.classroom.myClassroomList,
      classroomWorkList: state => state.classroom.classroomWorkList,
    }),
  },
  mounted() {
    this.$nextTick(() => {
      const swiperTop = this.$refs.swiperTop.swiper;
      const swiperThumbs = this.$refs.swiperThumbs.swiper;
      swiperTop.controller.control = swiperThumbs;
      swiperThumbs.controller.control = swiperTop;
    });
    this.fetchClassroomList();
  },
  methods: {
    isShowClassroomContent(classroom) {
      if (classroom.classmate.join_status == 'approved') return true;
      if (classroom.classmate.join_status == 'owner') return true;
      return false;
    },
    openWorkDetail(work) {
      this.selectedWork = work;
      this.workDialogVisible = true;
    },
    closeWorkDetailDialog() {
      this.workDialogVisible = false;
    },
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
