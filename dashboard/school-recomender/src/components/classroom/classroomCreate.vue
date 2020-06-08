<template>
  <v-card
    class="elevation-6"
    height="100%"
    width="100%"
  >
    <v-card-title />
    <v-card-text class="mt-3">
      <p
        v-show="error"
        id="error"
      >
        {{ error }}
      </p>
      <p>{{ message }}</p>
      <label>
        <v-img
          v-if="classroomImage"
          :src="classroomImage"
          class="classroom_image"
        />
        <v-img
          v-else
          src="@/assets/classroom-top_small.png"
          class="classroom_image"
        />
        <div>
          <input
            id="classroom_image"
            type="file"
            accept="image/*"
            @change="onClassroomImageChange"
          >
        </div>
      </label>
      <v-form class="mt-3">
        <v-text-field
          v-model="classroomName"
          counter="25"
          label="クラス名"
          required
        />
        <v-text-field
          v-model="classroomExplain"
          counter="25"
          label="クラス説明"
          required
        />
        <v-combobox
          v-model="classroomTagList"
          label="タグ（複数追加可）"
          multiple
          required
          chips
        />
        <v-checkbox
          v-model="counterEn"
          label="定員を設ける"
          class="mb-0"
        />
        <v-text-field
          v-model.number="classroomMemberCapacity"
          :disabled="!counterEn"
          :rules="[v => Math.sign(v) || '定員は半角数字を入力してください']"
          label="定員"
          dense
          class="mt-0"
          required
        />

        <v-checkbox
          v-model="secret"
          label="非公開にする"
          required
        />
      </v-form>
    </v-card-text>
    <v-card-actions>
      <v-spacer />
      <v-btn
        color="yellow darken-1"
        block
        large
        :loading="loading"
        :disabled="loading"
        @click="classroomCreate"
      >
        作成
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
import "@mdi/font/css/materialdesignicons.css";
export default {
  name: "ClassroomCreate",
  data: () => ({
    classroomImage: "",
    classroomImageUrl: null,
    selectedImage: null,
    classroomName: "",
    classroomExplain: null,
    classroomTagList: [],
    counterEn: false,
    classroomMemberCapacity: null,
    secret: false,
    loading: false,
    message: "",
    error: ""
  }),
  methods: {
    setError(error, text) {
      this.error =
        (error.response && error.response.data && error.response.data.error) ||
        text;
    },
    getBase64(file) {
      return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onload = () => resolve(reader.result);
        reader.onerror = error => reject(error);
      });
    },
    onClassroomImageChange(e) {
      const images = e.target.files || e.dataTransfer.files;
      this.$store
        .dispatch("putS3PublicFile", {
        file: images[0]})
        .then((s3Key) => {
          this.classroomImageUrl = s3Key.replace("upload/", "");
          this.$store.dispatch("getS3PublicFile", s3Key)
            .then(url => {
              this.classroomImage = url;
            })
        })
        .catch(err => {
          console.log(err)
          this.setError(err, "画像のアップロードに失敗しました。")
        });
    },
    classroomCreate() {
      this.loading = true;
      this.$store
        .dispatch("classroom/createClassroom", {
          imageUrl: this.classroomImageUrl,
          name: this.classroomName,
          tagList: this.classroomTagList,
          isSecret: this.secret,
          capacity: this.classroomMemberCapacity,
          caption: this.classroomExplain,
        })
        .then(result => {
          console.log(result)
          this.loading = false;
          this.$emit("classroomCreated");
        })
        .catch(err => {
          this.loading = false;
          console.log(err);
        });
    }
  }
};
</script>

<style lang="scss">
.classroom_image {
  cursor: pointer;
}
.classroom_image:hover {
  opacity: 0.7;
}
</style>
