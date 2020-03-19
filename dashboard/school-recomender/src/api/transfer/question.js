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
    "estimated_time": questionInput.estimatedTime,
    "question_sentence": {
        "text": sentenceText,
        "image_url": questionInput.sentence.imageUrl},
    "question_answer": {
        "text": answerText,
        "image_url": questionInput.answer.imageUrl},
    "question_commentary": {
        "text": commentaryText,
        "image_url": questionInput.commentary.imageUrl},
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
    if (subjectName === '世界史') return 'world_history';
    if (subjectName === '日本史') return 'japanease_history';
    if (subjectName === '地理') return 'geography';
    if (subjectName === '現代社会') return 'contemporary_society';
    if (subjectName === '物理') return 'physics';
    if (subjectName === '化学') return 'chemistry';
    if (subjectName === '生物') return 'biology';
    if (subjectName === '地学') return 'earth_science';
  },
  getSubjectNameFromType(subjectType){
    if (subjectType === 'japanease') return '国語';
    if (subjectType === 'math') return '数学';
    if (subjectType === 'english') return '英語';
    if (subjectType === 'world_history') return '世界史';
    if (subjectType === 'japanease_history') return '日本史';
    if (subjectType === 'geography') return '地理';
    if (subjectType === 'contemporary_society') return '現代社会';
    if (subjectType === 'physics') return '物理';
    if (subjectType === 'chemistry') return '化学';
    if (subjectType === 'biology') return '生物';
    if (subjectType === 'earth_science') return '地学';
  },
  getSubjectNameList(){
    return [
      '国語', '数学', '英語', '世界史', '日本史',
      '地理', '現代社会', '物理', '化学', '生物', '地学'
    ]
  },
  getQuestionModel() {
    return {
      "estimated_time": 0,
      "question_answer": {
        "image_url": "",
        "text": ""
      },
      "question_commentary": {
        "image_url": "",
        "text": ""
      },
      "question_id": 0,
      "question_sentence": {
        "image_url": "",
        "summary": "",
        "text": ""
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
