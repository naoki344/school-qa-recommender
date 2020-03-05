<!-- The ref attr used to find the swiper instance -->
<template>
  <v-container>
    <swiper class="classroom-swiper-thumbs" :options="swiperOptionThumbs" ref="swiperThumbs">
      <swiper-slide>クラス1</swiper-slide>
    </swiper>
    <swiper :options="swiperOptionTop" ref="swiperTop">
      <swiper-slide>
        <QuestionIndex />
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
import 'swiper/dist/css/swiper.css'
import { swiper, swiperSlide } from 'vue-awesome-swiper'
import QuestionIndex from "@/components/QuestionIndex.vue";

export default {
  name: "classroomSwiper",
  components: {
    swiper,
    swiperSlide,
    QuestionIndex
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
  },
  mounted() {
    this.$nextTick(() => {
      const swiperTop = this.$refs.swiperTop.swiper
      const swiperThumbs = this.$refs.swiperThumbs.swiper
      swiperTop.controller.control = swiperThumbs
      swiperThumbs.controller.control = swiperTop
    })
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
