from dataclasses import dataclass
from typing import List

from app.model.classroom.classmate import Classmate
from app.model.classroom.classmate import ClassmateList
from app.model.classroom.classroom import Classroom


@dataclass(frozen=True)
class MyClassroom:
    classroom: Classroom
    classmate: Classmate
    classmate_list: ClassmateList

    def from_dict(data: dict) -> 'MyClassroom':
        return MyClassroom(classroom=Classroom.from_dict(data["classroom"]),
                           classmate=Classmate.from_dict(data["classmate"]),
                           classmate_list=ClassmateList.from_list(
                               data["classmate_list"]))

    def to_dict(self) -> dict:
        return {
            "classroom": self.classroom.to_dict(),
            "classmate": self.classmate.to_dict(),
            "classmate_list": self.classmate_list.to_list()
        }

    def to_response(self) -> dict:
        data = {
            "classroom": self.classroom.to_dict(),
            "classmate": self.classmate.to_dict(),
        }
        if self.classmate.join_status.is_join:
            data = {**data, "classmate_list": self.classmate_list.to_list()}
        return data


@dataclass(frozen=True)
class MyClassroomList:
    values: List[MyClassroom]

    @staticmethod
    def from_list(data) -> 'MyClassroomList':
        return MyClassroomList([MyClassroom.from_dict(d) for d in data])

    def to_list(self) -> List[dict]:
        return [s.to_dict() for s in self.values]

    def to_response(self) -> List[dict]:
        return [s.to_response() for s in self.values]
