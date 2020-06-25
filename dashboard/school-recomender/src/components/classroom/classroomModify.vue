<template>
  <v-card
    class="elevation-6"
    width="100%"
  >
    <v-card-title class="pa-3">
      <v-btn icon>
        <v-icon>mdi-close</v-icon>
      </v-btn>
      <v-spacer />
      <h4 class="card-title-item">
        クラス情報を編集
      </h4>
      <v-spacer />
      <v-btn
        color="yellow darken-1"
        :loading="loading"
        :disabled="!inputFormIsValid"
        @click="classroomModify"
      >
        保存
      </v-btn>
    </v-card-title>
    <v-divider />
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
          v-if="classroomForm.imageUrl != ''"
          :src="classroomForm.imageUrl"
          class="classroom_image"
        />
        <v-img
          v-else-if="getImageUrlW512(modifyClassroom)"
          :src="imageListW512[modifyClassroom.image_url]"
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
      <v-form
        ref="form"
        v-model="inputFormIsValid"
        class="mt-3"
        lazy-validation
      >
        <v-text-field
          v-model="classroomForm.name"
          label="クラス名"
          required
          :rules="[rules.required]"
        />
        <v-text-field
          v-model="classroomForm.caption"
          label="クラス説明"
          required
          :rules="[rules.required]"
        />
        <v-combobox
          v-model="classroomForm.tagList"
          label="タグ（複数追加可）"
          multiple
          required
          chips
          :rules="[rules.required]"
        />
        <v-checkbox
          v-model="classroomForm.counterEn"
          label="定員を設ける"
          class="mb-0"
        />
        <v-text-field
          v-if="classroomForm.counterEn"
          v-model.number="classroomForm.capacity"
          :disabled="!classroomForm.counterEn"
          :rules="[(v) => Math.sign(v) || '定員は半角数字を入力してください']"
          label="定員"
          dense
          class="mt-0"
          required
        />
        <v-checkbox
          v-model="classroomForm.secret"
          label="非公開にする"
          required
        />
      </v-form>
    </v-card-text>
  </v-card>
</template>

<script>
import "@mdi/font/css/materialdesignicons.css";
import schoolApiClassroomTransfer from "@/api/transfer/classroom.js";
export default {
  name: "ClassroomModify",
  props: {
    modifyClassroom: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      classroomForm: {
        imageUrl: "",
        s3Key: "",
        name: "",
        caption: "",
        tagList: [],
        capacity: "",
        secret: true,
        counterEn: false
      },
      imageListW512: [],
      message: "",
      error: "",
      inputFormIsValid: false,
      rules: {
        required: value => !!value || "入力されていません"
      },
      loading: false
    };
  },
  created() {
    this.classroomForm = schoolApiClassroomTransfer.toFormData(
      this.modifyClassroom
    );
  },
  methods: {
    setError(error, text) {
      this.classroomForm.error =
        (error.response && error.response.data && error.response.data.error) ||
        text;
    },
    getBase64(file) {
      return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onload = () => resolve(reader.result);
        reader.onerror = error => reject(classroomForm.error);
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
    onClassroomImageChange(e) {
      const images = e.target.files || e.dataTransfer.files;
      this.$store
        .dispatch("putS3PublicFile", {
          file: images[0]
        })
        .then(s3Key => {
          this.classroomForm.s3Key = s3Key.replace("upload/", "");
          this.$store.dispatch("getS3PublicFile", s3Key).then(url => {
            this.classroomForm.imageUrl = url;
          });
        })
        .catch(err => {
          console.log(err);
          this.setError(err, "画像のアップロードに失敗しました。");
        });
    },
    classroomModify() {
      this.classroomForm.inputFormIsValid = this.$refs.form.validate();
      if (this.classroomForm.inputFormIsValid === false) return;
      this.loading = true;
      let imageUrl = this.modifyClassroom.image_url;
      if (this.classroomForm.s3Key != null) {
        imageUrl = this.classroomForm.s3Key;
      }
      this.$store
        .dispatch("classroom/modifyClassroom", {
          classroomId: this.modifyClassroom.classroom_id,
          inputData: {
            imageUrl: imageUrl,
            name: this.classroomForm.name,
            tagList: this.classroomForm.tagList,
            isSecret: this.classroomForm.secret,
            capacity: this.classroomForm.capacity,
            caption: this.classroomForm.caption
          }
        })
        .then(result => {
          this.loading = false;
          this.$emit("classroomModified");
          this.classroomForm = JSON.parse(JSON.stringify(classroomFormInit));
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
.card-title-item {
  text-align: center;
  margin: 0 auto;
}
</style>
