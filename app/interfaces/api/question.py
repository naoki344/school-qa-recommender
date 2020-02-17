import json
import os
from logging import getLogger
from app.application.usecase.question import CreateQuestion
from app.application.usecase.question import UpdateQuestion
from app.application.usecase.question import FindQuestion
from app.application.usecase.question import GetQuestionList
from app.model.question.question import Question
from app.model.question.question import QuestionId
from app.model.question.question import RegisterUserId
from app.configure.usecase.question import create_question
from app.configure.usecase.question import update_question
from app.configure.usecase.question import find_question
from app.configure.usecase.question import get_question_list
from app.interfaces.api.response import APIGatewayResponse

stage_name = os.environ['STAGE_NAME']


def create_question_handler(event, context):
    data = json.loads(event["body"])
    service: CreateQuestion = create_question(
        stage_name=stage_name, logger=getLogger())
    question = service.run(data)
    return APIGatewayResponse.to_response(
        question.to_dict())


def update_question_handler(event, context):
    path = event["pathParameters"]
    question_id = QuestionId(int(path["question_id"]))

    data = json.loads(event["body"])
    service: UpdateQuestion = update_question(
        stage_name=stage_name, logger=getLogger())
    question = service.run(question_id, data)
    return APIGatewayResponse.to_response(
        question.to_dict())


def get_question_list_handler(event, context):
    logger = getLogger()
    register_user_id = RegisterUserId('fjeiwo0g-rfar-fae')
    service: GetQuestionList = get_question_list(
        stage_name=stage_name, logger=logger)
    question_list, paging_key = service.run(
        register_user_id=register_user_id)
    data = {
        "question_card_list":
        [d.to_dict() for d in question_list],
            "paging_key": paging_key}
    return APIGatewayResponse.to_response(data)


def find_question_handler(event, context):
    path = event["pathParameters"]
    question_id = QuestionId(int(path["question_id"]))
    logger = getLogger()
    service: FindQuestion = find_question(
        stage_name=stage_name, logger=logger)
    question = service.run(question_id)
    return APIGatewayResponse.to_response(
        question.to_dict())
