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
        <div class="classroom-swiper-thumbs-box">
          <v-card shaped>
            <v-img
              v-if="getImageUrl(myClass.classroom)"
              class="white--text align-end classroom-swiper-thumbs-image"
              :src="imageList[myClass.classroom.image_url]"
            >
              <v-card-title>
                <h3>{{ myClass.classroom.name }}</h3>
              </v-card-title>
            </v-img>
          </v-card>
        </div>
      </swiper-slide>
    </swiper>
    <swiper
      ref="swiperTop"
      :options="swiperOptionTop"
      class="pa-0 classroom-swiper-content"
    >
      <swiper-slide
        v-for="myClass in classroomList"
        :key="myClass.classroom.classroom_id"
        style="text-align: left;"
      >
        <div v-if="isShowClassroomContent(myClass)">
          <v-subheader>ワーク一覧</v-subheader>
          <v-divider />
          <v-list
            subheader
            two-line
          >
            <div
              v-for="item in classroomWorkList[myClass.classroom.classroom_id]"
              :key="item.work_id"
              subheader
              two-line
            >
              <v-list-item
                link
                class="classroom-work-list-item"
                @click="openWorkDetail(item, myClass)"
              >
                <div class="classroom-work-list-item-image">
                  <v-img
                    v-if="getImageUrl(item)"
                    class=""
                    width="80"
                    min-height="60"
                    :src="imageList[item.image_url]"
                  />
                </div>
                <v-list-item-content
                  class="pa-0"
                >
                  <v-list-item-title>{{ item.title }}</v-list-item-title>
                  <v-list-item-subtitle>{{ item.caption }}</v-list-item-subtitle>
                </v-list-item-content>
              </v-list-item>
              <v-divider />
            </div>
          </v-list>
        </div>
      </swiper-slide>
    </swiper>
    <classroom-work-detail-dialog
      :work="selectedWork"
      :classroom="selectedClass"
      :dialog-visible="workDialogVisible"
      @closeDialog="closeWorkDetailDialog()"
    />
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
      swiperOptionTop: {
        slidesPerView: 'auto',
        centeredSlides: true,
      },
      imageList: [],
      selectedWork: '',
      selectedClass: '',
      swiperOptionThumbs: {
        speed: 500,
        slidesPerView: "auto",
        spaceBetween: 20,
        centeredSlides: true,
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
    openWorkDetail(work, myClass) {
      this.selectedWork = work;
      this.selectedClass = myClass.classroom;
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
.swiper {
  height: 300px;
  width: 100%;

  .swiper-slide {
    display: flex;
    justify-content: center;
    align-items: center;
    text-align: center;
    font-weight: bold;
  }
}
.classroom-swiper-thumbs {
  .swiper-slide {
    width: 80%;
  }
  .classroom-swiper-thumbs-image {
     width: 100%;
     max-height: 180px;
     margin: auto;
     margin-bottom: 15px;
  }
  .v-card {
    border-radius: 12px;
  }
  .v-card__title {
    padding: 12px;
	display: flex;
    justify-content: flex-end;
	background-color: rgb(0, 0, 0, 0.5);
	h3 {
      font-weight: 300;
	  marign-bottom: 0;
      line-height: 1;
	}
  }
}
.swiper-slide-next, .swiper-slide-prev {
  .classroom-swiper-thumbs-box {
    .classroom-swiper-thumbs-image {
       max-height: 160px;
	   margin: 10px 0;
    }
  }
}

.classroom-work-list-item {
  padding: 10px 15px;
  .classroom-work-list-item-image {
    width: 80px;
    height: 100%;
  }
  .v-list-item__title {
    font-size: 1.4;
    font-weight: 600;
	margin-bottom: 5px;
  }
  .v-list-item__content {
    margin-left: 10px;
  }
  .v-list-item__subtitle {
    white-space: pre-line;
    max-height: 2rem;
    overflow: hidden;
  }
}
</style>
