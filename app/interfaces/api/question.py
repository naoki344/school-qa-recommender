import json
import os
from logging import getLogger
from app.application.usecase.question import CreateQuestion
from app.model.question.question import Question
from app.model.question.question import QuestionId
from app.configure.usecase.question import create_question
from app.configure.usecase.question import update_question
from app.configure.usecase.question import find_question

stage_name = os.environ['STAGE_NAME']


def create_question_handler(event, context):
    data = json.loads(event["body"])
    service: CreateQuestion = create_question(
        stage_name=stage_name, logger=getLogger())
    question = service.run(data)
    return {
        "statusCode": 200,
        "body": json.dumps(question.to_dict()),
        "headers": {
            "Access-Control-Allow-Origin": "*"
        },
    }


def update_question_handler(event, context):
    path = event["pathParameters"]
    question_id = QuestionId(int(path["question_id"]))

    data = json.loads(event["body"])
    service: CreateQuestion = update_question(
        stage_name=stage_name, logger=getLogger())
    question = service.run(question_id, data)
    return {
        "statusCode": 200,
        "body": json.dumps(question.to_dict()),
        "headers": {
            "Access-Control-Allow-Origin": "*"
        },
    }


def find_question_handler(event, context):
    path = event["pathParameters"]
    question_id = QuestionId(int(path["question_id"]))
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
