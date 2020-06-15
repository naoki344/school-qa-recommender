<template>
  <v-card class="elevation-6" height="100%" width="100%">
    <v-card-title />
    <v-card-text class="mt-3">
      <p v-show="error" id="error">{{ error }}</p>
      <p>{{ message }}</p>
      <label>
        <v-img
          v-if="classroomForm.classroomImage"
          :src="classroomForm.classroomImage"
          class="classroom_image"
        />
        <v-img v-else src="@/assets/classroom-top_small.png" class="classroom_image" />
        <div>
          <input id="classroom_image" type="file" accept="image/*" @change="onClassroomImageChange" />
        </div>
      </label>
      <p>{{modifyClassroom}}</p>
      <v-form ref="form" v-model="inputFormIsValid" class="mt-3" lazy-validation>
        <v-text-field
          v-model="classroomForm.classroomName"
          label="クラス名"
          required
          :rules="[rules.required]"
        />
        <v-text-field
          v-model="classroomForm.classroomExplain"
          label="クラス説明"
          required
          :rules="[rules.required]"
        />
        <v-combobox
          v-model="classroomForm.classroomTagList"
          label="タグ（複数追加可）"
          multiple
          required
          chips
          :rules="[rules.required]"
        />
        <v-checkbox v-model="classroomForm.counterEn" label="定員を設ける" class="mb-0" />
        <v-text-field
          v-if="classroomForm.counterEn"
          v-model.number="classroomForm.classroomMemberCapacity"
          :disabled="!classroomForm.counterEn"
          :rules="[(v) => Math.sign(v) || '定員は半角数字を入力してください']"
          label="定員"
          dense
          class="mt-0"
          required
        />

        <v-checkbox v-model="classroomForm.secret" label="非公開にする" required />
      </v-form>
    </v-card-text>
    <v-card-actions>
      <v-spacer />
      <v-btn
        color="yellow darken-1"
        block
        large
        :loading="loading"
        :disabled="!classroomForm.inputFormIsValid"
        @click="classroomCreate"
      >作成</v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
import "@mdi/font/css/materialdesignicons.css";
import schoolApiClassroomTransfer from "@/api/transfer/classroom.js";
export default {
  name: "ClassroomModify",
  data() {
    return {
      classroomForm: {
        imageUrl: null,
        name: this.modifyClassroom.name,
        explain: this.modifyClassroom.caption,
        tagList: this.modifyClassroom.tag_list,
        capacity: this.modifyClassroom.capacity,
        secret: false
      },
      counterEn: 10,
      classroomImage: "",
      selectedImage: null,
      message: "",
      error: "",
      inputFormIsValid: false,
      rules: {
        required: value => !!value || "入力されていません"
      },
      loading: false
    };
  },
  props: {
    modifyClassroom: Object
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
    onClassroomImageChange(e) {
      const images = e.target.files || e.dataTransfer.files;
      this.$store
        .dispatch("putS3PublicFile", {
          file: images[0]
        })
        .then(s3Key => {
          this.classroomImageUrl = s3Key.replace("upload/", "");
          this.$store.dispatch("getS3PublicFile", s3Key).then(url => {
            this.classroomImage = url;
          });
        })
        .catch(err => {
          console.log(err);
          this.setError(err, "画像のアップロードに失敗しました。");
        });
    },
    classroomCreate() {
      this.classroomForm.inputFormIsValid = this.$refs.form.validate();
      if (this.classroomForm.inputFormIsValid === false) return;
      this.loading = true;
      this.$store
        .dispatch("classroom/createClassroom", {
          imageUrl: this.classroomForm.classroomImageUrl,
          name: this.classroomForm.classroomName,
          tagList: this.classroomForm.classroomTagList,
          isSecret: this.classroomForm.secret,
          capacity: this.classroomForm.classroomMemberCapacity,
          caption: this.classroomForm.classroomExplain
        })
        .then(result => {
          console.log(result);
          this.loading = false;
          this.$emit("classroomCreated");
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
</style>
