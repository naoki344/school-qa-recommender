export default {
  toRequest(inputData) {
    let publishType = "private";
    if (inputData.isSecret === false) {
      publishType = "public";
    }
    return {
      "name": inputData.name,
      "image_url": inputData.imageUrl,
      "tag_list": inputData.tagList,
      "publish_type": publishType,
      "capacity": inputData.capacity,
      "caption": inputData.caption,
    }
  },
  toFormData(data) {
    let publish_type = true;
    if (data.publish_type === "public") {
      publish_type = false;
    }
    let counterEn = false;
    if (data.capacity != null) {
      counterEn = true
    }
    return {
      "name": data.name,
      "imageUrl": "",
      "tagList": data.tag_list,
      "secret": publish_type,
      "capacity": data.capacity,
      "caption": data.caption,
      "counterEn": counterEn
    }
  }
}
