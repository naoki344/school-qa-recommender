<template>
  <v-container>
    <v-col>
      <label for="avatarImage">
        <v-avatar color="indigo" size="66">
          <v-icon v-if="cropImg == ''" dark>mdi-account-circle</v-icon>
          <v-img
            v-if="cropImg != ''"
            class="round"
            :src="cropImg"
            style="width: yoko; height: tate; border: 1px solid gray;"
            alt="Cropped Image"
          />
        </v-avatar>
        <h4>画像を選択</h4>
      </label>
      <input
        type="file"
        name="image"
        accept="image/*"
        id="avatarImage"
        @change="setImage"
        @click="openDialog"
        style="display:none;"
      />
      <v-dialog v-model="dialog" persistent v-if="imgSrc != ''" max-width="460">
        <v-card>
          <v-divider></v-divider>
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
              ></vue-cropper>
            </div>
          </v-card-text>
          <v-card-actions>
            <v-btn color="grey lighten-1" @click="dialog=false">戻る</v-btn>
            <v-spacer />
            <v-btn color="yellow darken-1" @click="cropImage">適用する</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-col>
  </v-container>
</template>

<script>
import VueCropper from "vue-cropperjs";
import "cropperjs/dist/cropper.css";
import "@mdi/font/css/materialdesignicons.css";
export default {
  name: "avatarCreate",
  components: {
    VueCropper
  },
  data() {
    return {
      yoko: 1,
      tate: 1,
      imgSrc: "",
      cropImg: "",
      filename: "",
      dialog: false
    };
  },
  methods: {
    appendIconCallback() {
      alert("click:append");
    },
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
      this.cropImg = this.$refs.cropper.getCroppedCanvas().toDataURL();
      this.dialog = false;
    }
  }
};
</script>

<style scoped>
.round {
  border-radius: 50%;
}
</style>
