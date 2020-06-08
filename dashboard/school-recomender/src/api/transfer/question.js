import moment from "moment";

export default {
  toRequest(questionInput){
    var sentenceText = ''
    if (questionInput.contents == '') {
        sentenceText = '-'
    } else {
        sentenceText = questionInput.contents
    }
    return {
    "estimated_time": questionInput.estimatedTime,
    "question_sentence": {
        "contents": sentenceText,
	},
    "register_date": moment().utc().format(),
    "subject_name": questionInput.subjectName,
    "question_type": questionInput.questionType,
    "sort_tag_list": questionInput.sortTagList
    }
  },
  getSubjectNameList(){
    return [
      '国語', '数学', '英語', '世界史', '日本史',
      '地理', '現代社会', '物理', '化学', '生物', '地学'
    ]
  },
  getQuestionModel() {
    return {
      "question_id": 0,
      "question_sentence": {
        "summary": "",
        "contents": ""
      },
      "question_type": "",
      "register_date": "",
      "register_user_id": "",
      "register_user_name": "",
      "sort_tag_list": [],
      "subject_type": ""
    } 
  }
}
