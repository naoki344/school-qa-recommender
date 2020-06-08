from dataclasses import dataclass
from enum import Enum
from enum import auto
from typing import List
from typing import Optional

from app.model.classroom.owner import ClassroomOwnerList
from app.model.user.user import User
from app.model.user.user import UserId


@dataclass(frozen=True)
class ClassroomId:
    value: int


@dataclass(frozen=True)
class ClassroomName:
    value: str


@dataclass(frozen=True)
class ClassroomCaption:
    value: str


@dataclass(frozen=True)
class ClassroomImageUrl:
    value: str


@dataclass(frozen=True)
class ClassroomPublishType(Enum):
    public = auto()
    private = auto()


@dataclass(frozen=True)
class ClassroomTag:
    value: str


@dataclass(frozen=True)
class ClassroomTagList:
    values: List[ClassroomTag]

    @staticmethod
    def from_list(data) -> 'ClassroomTagList':
        return ClassroomTagList([ClassroomTag(str(d)) for d in data])

    def to_list(self) -> List[str]:
        return [s.value for s in self.values]


@dataclass(frozen=True)
class ClassroomCapacity:
    value: int


@dataclass(frozen=True)
class Classroom:
    classroom_id: ClassroomId
    name: ClassroomName
    owner_list: ClassroomOwnerList
    image_url: ClassroomImageUrl
    publish_type: ClassroomPublishType
    tag_list: ClassroomTagList
    capacity: Optional[ClassroomCapacity]
    caption: Optional[ClassroomCaption]

    @staticmethod
    def from_dict(data) -> 'Classroom':
        return Classroom(
            classroom_id=ClassroomId(int(data['classroom_id'])),
            name=ClassroomName(str(data['name'])),
            owner_list=ClassroomOwnerList.from_list(data['owner_list']),
            image_url=ClassroomImageUrl(str(data['image_url'])),
            tag_list=ClassroomTagList.from_list(data['tag_list']),
            publish_type=ClassroomPublishType[str(data['publish_type'])],
            capacity=ClassroomCapacity(int(data['capacity']))
            if data.get('capacity') else None,
            caption=ClassroomCaption(str(data['caption']))
            if data.get('caption') else None)

    def to_dict(self) -> dict:
        return {
            'classroom_id': self.classroom_id.value,
            'name': self.name.value,
            'owner_list': self.owner_list.to_list(),
            'image_url': self.image_url.value,
            'publish_type': self.publish_type.name,
            'tag_list': self.tag_list.to_list(),
            'capacity': self.capacity.value if self.capacity else None,
            'caption': self.caption.value if self.caption else None
        }

    @staticmethod
    def create(classroom_id: int, user: User, data: dict) -> 'Classroom':
        return Classroom(classroom_id=ClassroomId(int(classroom_id)),
                         name=ClassroomName(str(data['name'])),
                         owner_list=ClassroomOwnerList.create(user),
                         image_url=ClassroomImageUrl(str(data['image_url']))
                         if data.get('image_url') else
                         ClassroomImageUrl('classroom-default-image.png'),
                         tag_list=ClassroomTagList.from_list(data['tag_list']),
                         publish_type=ClassroomPublishType[str(
                             data['publish_type'])],
                         capacity=ClassroomCapacity(int(data['capacity']))
                         if data.get('capacity') else None,
                         caption=ClassroomCaption(str(data['caption']))
                         if data.get('caption') else None)

    def can_join_request(self) -> bool:
        if self.publish_type is ClassroomPublishType.public:
            return True
        return False

    def is_owner(self, user_id: UserId) -> bool:
        return self.owner_list.is_owner(user_id)
