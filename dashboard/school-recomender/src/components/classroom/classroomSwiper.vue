<!-- The ref attr used to find the swiper instance -->
<template>
  <v-content>
    <div v-if="existsJoinClassroom">
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
                v-if="getImageUrlW512(myClass.classroom)"
                class="white--text align-end classroom-swiper-thumbs-image"
                :src="imageListW512[myClass.classroom.image_url]"
              >
                <v-card-title>
                  <h3>{{ myClass.classroom.name }}</h3>
                </v-card-title>
              </v-img>
              <v-img
                v-else
                class="white--text align-end classroom-swiper-thumbs-image"
                src="@/assets/classroom-top_small.png"
              />
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
              style="margin-bottom: 50px;"
            >
              <div
                v-for="item in classroomWorkList[
                  myClass.classroom.classroom_id
                ]"
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
                      v-if="getImageUrlH60(item)"
                      class
                      width="80"
                      min-height="60"
                      :src="imageListH60[item.image_url]"
                    />
                  </div>
                  <v-list-item-content class="pa-0">
                    <v-list-item-title>{{ item.title }}</v-list-item-title>
                    <v-list-item-subtitle>
                      {{
                        item.caption
                      }}
                    </v-list-item-subtitle>
                  </v-list-item-content>
                </v-list-item>
                <v-divider />
              </div>
            </v-list>
            <v-subheader class="create-approve-join-request-header">
              クラスメイト一覧
              <div class="create-approve-join-request-link">
                <a>招待用リンクを取得</a>
              </div>
            </v-subheader>
            <v-divider />
            <v-list
              subheader
              two-line
              style="margin-bottom: 50px;"
            >
              <div
                v-for="classmate in myClass.classmate_list"
                :key="classmate.user_id"
                subheader
                two-line
              >
                <v-list-item
                  link
                  class="classmate-list-item"
                >
                  <v-avatar
                    tile
                    size="40"
                  >
                    <v-img :src="getUserAvatarImageUrl(classmate.user_id)" />
                  </v-avatar>
                  <v-list-item-content class="pa-0">
                    <div>
                      {{ classmate.nickname }}
                      <span>
                        {{
                          classmate.join_status | joinStatusFilter
                        }}
                      </span>
                    </div>
                  </v-list-item-content>
                  <v-list-item-content
                    v-if="classmate.join_status === 'requested'"
                    class="pa-0"
                  >
                    <div class="approve-join-request-text">
                      <a
                        @click="
                          approveJoinRequest(
                            myClass.classroom.classroom_id,
                            classmate.user_id,
                            classmate.nickname
                          )
                        "
                      >参加を承認する</a>
                    </div>
                  </v-list-item-content>
                </v-list-item>
                <v-divider />
              </div>
            </v-list>
          </div>
        </swiper-slide>
      </swiper>
    </div>
    <div v-else>
      <div class="classroom-swiper-thumbs-box join-classroom-nothing-image">
        <v-card shaped>
          <v-img
            class="white--text align-end classroom-swiper-thumbs-image"
            src="@/assets/classroom-top_small.png"
          />
        </v-card>
      </div>
      <v-divider />
      <p class="ma-4">
        現在参加中のクラスはありません。
      </p>
    </div>
  </v-content>
</template>

<script>
import { mapState } from "vuex";
import "swiper/dist/css/swiper.css";
import { swiper, swiperSlide } from "vue-awesome-swiper";
import { components } from "aws-amplify-vue";

export default {
  name: "ClassroomSwiper",
  components: {
    swiper,
    swiperSlide,
    ...components
  },
  filters: {
    joinStatusFilter(value) {
      if (value === "") return "";
      if (value === "approved") return "参加中";
      if (value === "owner") return "オーナー";
      if (value === "requested") return "承認待ち";
    }
  },
  data() {
    return {
      file: null,
      url: "",
      swiperOptionTop: {
        slidesPerView: "auto",
        centeredSlides: true
      },
      imageListW512: [],
      imageListH60: [],
      selectedWorkId: "",
      selectedClassId: "",
      swiperOptionThumbs: {
        speed: 500,
        slidesPerView: "auto",
        spaceBetween: 20,
        centeredSlides: true
      },
      workDialogVisible: false,
      existsJoinClassroom: true
    };
  },
  computed: {
    ...mapState({
      classroomList: state => state.classroom.myClassroomList,
      classroomWorkList: state => state.classroom.classroomWorkList
    })
  },
  mounted() {
    this.fetchClassroomList();
    this.$nextTick(() => {
      const swiperTop = this.$refs.swiperTop.swiper;
      const swiperThumbs = this.$refs.swiperThumbs.swiper;
      swiperTop.controller.control = swiperThumbs;
      swiperThumbs.controller.control = swiperTop;
    });
  },
  methods: {
    isShowClassroomContent(classroom) {
      if (classroom.classmate.join_status == "approved") return true;
      if (classroom.classmate.join_status == "owner") return true;
      return false;
    },
    getUserAvatarImageUrl(userId) {
      return this.$store.getters["user/userAvatarImageUrl"](userId);
    },
    openWorkDetail(work, myClass) {
      this.selectedWorkId = work.work_id;
      this.selectedClassId = myClass.classroom.classroom_id;
      console.log(this.selectedWorkId);
      console.log(this.selectedClassId);
      this.$router.push({
        name: "classroomWorkDetailPage",
        query: {
          work_id: this.selectedWorkId,
          classroom_id: this.selectedClassId
        }
      });
    },
    closeWorkDetailDialog() {
      this.workDialogVisible = false;
    },
    async fetchClassroomList() {
      this.$store.dispatch("classroom/fetchMyClassroomList").then(() => {
        if (this.classroomList.length == 0) {
          this.existsJoinClassroom = false;
        } else {
          this.existsJoinClassroom = true;
        }
      });
    },
    approveJoinRequest(classroomId, userId, nickName) {
      this.$store
        .dispatch("classroom/approveClassroomJoinRequest", {
          classroomId,
          userId
        })
        .then(data => {
          this.$store.dispatch("classroom/fetchMyClassroomList");
          alert(`${nickName} をクラスに追加しました。`);
        })
        .catch(err => {
          alert(
            `${nickName} のクラスに追加に失敗しました。(再度実行してくだください)`
          );
        });
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
    getImageUrlW512(obj) {
      if (obj["image_url"] == null) {
        return false;
      }
      const path = obj["image_url"];
      if (this.imageListW512[path] != null) {
        return true;
      }
      const thumbPath = "thumbnail/w512/" + path;
      this.$store
        .dispatch("getS3PublicFile", thumbPath)
        .then(url => {
          this.$set(this.imageListW512, path, url);
        })
        .catch(() => {
          return false;
        });
      return true;
    },
    getImageUrlH60(obj) {
      if (obj["image_url"] == null) {
        return false;
      }
      const path = obj["image_url"];
      if (this.imageListH60[path] != null) {
        return true;
      }
      const thumbPath = "thumbnail/h60/" + path;
      this.$store
        .dispatch("getS3PublicFile", thumbPath)
        .then(url => {
          this.$set(this.imageListH60, path, url);
        })
        .catch(() => {
          return false;
        });
      return true;
    }
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
}

.join-classroom-nothing-image {
  width: 80%;
  margin: 0 auto 20px auto;
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
    line-height: 1;
  }
}
.swiper-slide-next,
.swiper-slide-prev {
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

.classmate-list-item {
  font-weight: 600;
  margin: 0;
  span {
    font-size: 0.8rem;
    margin-left: 5px;
    font-weight: 300;
    color: rgba(0, 0, 0, 0.6);
  }
  .v-list-item__content {
    margin-left: 10px;
  }
  .approve-join-request-text {
    text-align: right;
    a {
      text-decoration: underline;
      color: #35a7ff;
    }
  }
}

.create-approve-join-request-header {
  display: flex;
  justify-content: space-between;
  a {
    text-decoration: underline;
    color: #35a7ff;
  }
  .create-approve-join-request-link {
    margin-top: 10px;
  }
}
</style>
