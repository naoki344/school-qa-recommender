from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from enum import auto
from typing import List
from typing import Optional


@dataclass(frozen=True)
class ClassRoomId:
    value: int


@dataclass(frozen=True)
class ClassRoomName:
    value: str


@dataclass(frozen=True)
class ClassRoomImageUrl:
    value: str


@dataclass(frozen=True)
class ClassRoomPublishType(Enum):
    public = auto()
    private = auto()


@dataclass(frozen=True)
class ClassRoomTag:
    value: str


@dataclass(frozen=True)
class ClassRoomTagList:
    values: List[ClassRoomTag]

    @staticmethod
    def from_list(data) -> 'ClassRoomTagList':
        return ClassRoomTagList([ClassRoomTag(str(d)) for d in data])

    def to_list(self) -> List[str]:
        return [s.value for s in self.values]


@dataclass(frozen=True)
class ClassRoomCapacity:
    value: int


@dataclass(frozen=True)
class ClassRoom:
    class_id: ClassRoomId
    name: ClassRoomName
    image_url: ClassRoomImageUrl
    publish_type: ClassRoomPublishType
    tag_list: ClassRoomTagList
    capacity: Optional[ClassRoomCapacity]

    @staticmethod
    def from_dict(data) -> 'ClassRoom':
        return ClassRoom(class_id=ClassRoomId(int(data['class_room_id'])),
                         name=ClassRoomName(str(data['name'])),
                         image_url=ClassRoomImageUrl(str(data['image_url'])),
                         tag_list=ClassRoomTagList.from_list(data['tag_list']),
                         publish_type=ClassRoomPublishType[str(
                             data['publish_type'])],
                         capacity=ClassRoomCapacity(int(data['capacity']))
                         if data.get('capacity') else None)

    def to_dict(self) -> dict:
        return {
            'class_room_id': self.class_id.value,
            'name': self.name.value,
            'image_url': self.image_url.value,
            'publish_type': self.publish_type.name,
            'tag_list': self.tag_list.to_list(),
            'capacity': self.capacity.value if self.capacity else None
        }
