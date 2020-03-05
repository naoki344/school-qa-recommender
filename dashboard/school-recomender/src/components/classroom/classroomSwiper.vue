<!-- The ref attr used to find the swiper instance -->
<template>
  <v-container>
    <swiper class="classroom-swiper-thumbs" :options="swiperOptionThumbs" ref="swiperThumbs">
      <swiper-slide v-for="(classroom, index) in classroomList" :key="index" >{{classroom.name}}</swiper-slide>
    </swiper>
    <swiper :options="swiperOptionTop" ref="swiperTop">
      <swiper-slide v-for="(classroom, index) in classroomList" :key="index" >
        <h1>{{classroom.name}}</h1>
      </swiper-slide>
      <!-- Optional controls -->
      <div class="swiper-pagination"  slot="pagination"></div>
      <div class="swiper-button-prev" slot="button-prev"></div>
      <div class="swiper-button-next" slot="button-next"></div>
      <div class="swiper-scrollbar"   slot="scrollbar"></div>
    </swiper>
  </v-container>
</template>

<script>
import { mapState } from "vuex";
import 'swiper/dist/css/swiper.css'
import { swiper, swiperSlide } from 'vue-awesome-swiper'

export default {
  name: "classroomSwiper",
  components: {
    swiper,
    swiperSlide,
  },
  data() {
    return {
      swiperOptionTop: {
        spaceBetween: 10,
        navigation: {
          nextEl: '.swiper-button-next',
          prevEl: '.swiper-button-prev'
        }
      },
      swiperOptionThumbs: {
        spaceBetween: 20,
        centeredSlides: true,
        slidesPerView: 'auto',
        touchRatio: 0.2,
        slideToClickedSlide: true,
		watchSlidesVisibility: true,
        watchSlidesProgress: true,
      }
    }
  },
  computed: {
    ...mapState({
      classroomList: state => state.classroom.classroomList
    })
  },
  methods: {
    fetchClassroomList() {
      this.$store.dispatch("classroom/fetchClassroomList");
    },
  },
  mounted() {
    this.$nextTick(() => {
      const swiperTop = this.$refs.swiperTop.swiper
      const swiperThumbs = this.$refs.swiperThumbs.swiper
      swiperTop.controller.control = swiperThumbs
      swiperThumbs.controller.control = swiperTop
    });
    this.fetchClassroomList();
  }
}
</script>


<style lang="scss" scoped >
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
