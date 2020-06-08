
export default {
  toRequest(inputData){
    console.log(inputData);
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
  }
}

