import json
import os
from logging import getLogger
from app.application.usecase.question import CreateQuestion
from app.model.question.question import Question
from app.model.question.question import QuestionId
from app.configure.usecase.question import create_question
from app.configure.usecase.question import find_question

stage_name = os.environ['STAGE_NAME']


def create_question_handler(event, context):
    question = Question.from_dict({
        'question_id': 1,
        'register_user_id': 30,
        'title': 'Test question Title',
        'contents': 'Test question Contents',
        'register_date': '2019-02-20 09:01:00.000+09:00',
        'subject_type': 'math',
        'caption': None
        })
    service: CreateQuestion = create_question(
        stage_name=stage_name, logger=getLogger())
    service.run(question)
    return {
        "statusCode": 200,
        "body": json.dumps(question.to_dict()),
        "headers": {
            "Access-Control-Allow-Origin": "*"
        },
    }


def find_question_handler(event, context):
    question_id = QuestionId(1)
    service: CreateQuestion = find_question(
        stage_name=stage_name, logger=getLogger())
    question = service.run(question_id)
    return {
        "statusCode": 200,
        "body": json.dumps(question.to_dict()),
        "headers": {
            "Access-Control-Allow-Origin": "*"
        },
    }
