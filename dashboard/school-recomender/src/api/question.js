import moment from "moment";

export default {
  toRequest(questionInput){
    var sentenceText = ''
    if (questionInput.sentence.text == '') {
        sentenceText = '-'
    } else {
        sentenceText = questionInput.sentence.text
    }
    var answerText = ''
    if (questionInput.answer.text == '') {
        answerText = '-'
    } else {
        answerText = questionInput.sentence.text
    }
    var commentaryText = ''
    if (questionInput.commentary.text == '') {
        commentaryText = '-'
    } else {
        commentaryText = questionInput.commentary.text
    }

    return {
    "register_user_id": "fjeiwo0g-rfar-fae",
    "register_user_name": "三好 直紀",
    "estimated_time": 15,
    "question_sentence": {
        "text": sentenceText,
        "image_url": ""},
    "question_answer": {
        "text": answerText,
        "image_url": ""},
    "question_commentary": {
        "text": commentaryText,
        "image_url": ""},
    "register_date": moment().utc().format(),
    "subject_type": this.getSubjectTypeFromName(questionInput.subjectName),
    "question_type": questionInput.questionType,
    "sort_tag_list": questionInput.sortTagList
    }
  },
  getSubjectTypeFromName(subjectName){
    if (subjectName === '国語') return 'japanease';
    if (subjectName === '数学') return 'math';
    if (subjectName === '英語') return 'english';
    if (subjectName === '化学') return 'chemistry';
  }
}
