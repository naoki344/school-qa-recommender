<template>
  <div>
    <v-container class="pt-0">
      <div
        class="pt-0"
        align="center"
      >
        <label for="avatarImage">
          <v-avatar
            class="avatar"
            color="indigo"
            size="66"
          >
            <v-icon
              v-if="cropedImageUrl == ''"
              dark
            >mdi-account-circle</v-icon>
            <v-img
              v-if="cropedImageUrl != ''"
              class="round"
              :src="cropedImageUrl"
              style="width: yoko; height: tate; border: 1px solid gray;"
              alt="Cropped Image"
            />
          </v-avatar>
          <br>
          <strong class="avatar">画像を選択</strong>
        </label>
        <input
          id="avatarImage"
          type="file"
          name="image"
          accept="image/*"
          style="display:none;"
          @change="setImage"
          @click="openDialog"
        >
      </div>
    </v-container>
    <v-dialog
      v-if="imgSrc != ''"
      v-model="dialog"
      persistent
      max-width="460"
    >
      <v-card>
        <v-divider />
        <v-card-text>
          <div
            v-if="imgSrc != ''"
            style="width: 100%; border: 1px solid gray; display: inline-block;"
          >
            <vue-cropper
              ref="cropper"
              :guides="true"
              :view-mode="2"
              drag-mode="crop"
              :auto-crop-area="1.0"
              :min-container-width="200"
              :min-container-height="200"
              :background="true"
              :rotatable="false"
              :src="imgSrc"
              :img-style="{ width: '100%' }"
              :aspect-ratio="yoko / tate"
            />
          </div>
        </v-card-text>
        <v-card-actions>
          <v-btn
            color="grey lighten-1"
            @click="dialog=false"
          >
            戻る
          </v-btn>
          <v-spacer />
          <v-btn
            color="yellow darken-1"
            @click="cropImage"
          >
            適用する
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import VueCropper from "vue-cropperjs";
import "cropperjs/dist/cropper.css";
import "@mdi/font/css/materialdesignicons.css";
export default {
  name: "AvatarCreate",
  components: {
    VueCropper
  },
  props: {
    cropedImageUrl: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      yoko: 1,
      tate: 1,
      imgSrc: "",
      filename: "",
      dialog: false
    };
  },
  methods: {
    openDialog() {
      this.dialog = true;
    },
    setImage(e) {
      const file = e.target.files[0];
      if (file == null) {
        return;
      }

      this.filename = file.name;
      if (!file.type.includes("image/")) {
        alert("Please select an image file");
        return;
      }
      if (typeof FileReader === "function") {
        const reader = new FileReader();
        reader.onload = event => {
          this.imgSrc = event.target.result;
          this.$refs.cropper.replace(event.target.result);
        };
        reader.readAsDataURL(file);
      } else {
        alert("Sorry, FileReader API not supported");
      }
    },
    cropImage() {
      const cropImg = this.$refs.cropper.getCroppedCanvas().toDataURL();
      this.$emit("changeCropedImage", cropImg);
      this.dialog = false;
    }
  }
};
</script>

<style scoped>
.round {
  border-radius: 50%;
}
.avatar:hover {
  cursor: pointer;
}
</style>
