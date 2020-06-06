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
      <v-form>
        <v-text-field
          v-model="classroomName"
          counter="25"
          label="クラス名"
          required
          dense
        />
        <v-text-field
          v-model="classroomExplain"
          counter="25"
          label="クラス説明"
          required
          dense
        />
        <v-text-field
          v-model="classroomTag"
          counter="25"
          label="タグ"
          required
          dense
        />
        <v-checkbox
          v-model="counterEn"
          class="ma-0 mr-2 ml-1"
          label="定員を設ける"
        />
        <v-text-field
          v-model.number="classroomMemberCapacity"
          :disabled="!counterEn"
          dense
          :rules="[v => !!v || 'You must agree to continue!']"
          label="定員"
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
    classroomName: "",
    classroomExplain: "",
    classroomTag: "",
    counterEn: false,
    classroomMemberCapacity: "",
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
      this.getBase64(images[0])
        .then(image => (this.classroomImage = image))
        .catch(error =>
          this.setError(error, "画像のアップロードに失敗しました。")
        );
    },
    classroomCreate() {
      this.loading = true;
      this.$store
        .dispatch("classroomCreate", {
          classroomImage: this.classroomImage,
          classroomName: this.classroomName,
          classroomExplain: this.classroomExplain,
          classroomTag: this.classroomTag,
          checkbox: this.secret,
          classroomMemberCapacity: this.classroomMemberCapacity
        })
        .then(() => {
          this.loading = false;
          this.$emit("closeclassroomCreateDialog");
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