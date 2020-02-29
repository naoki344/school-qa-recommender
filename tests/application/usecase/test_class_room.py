from copy import deepcopy
from unittest import TestCase
from unittest.mock import MagicMock

from app.application.query.user import UserQueryService
from app.application.usecase.class_room import CreateClassRoom
from app.application.usecase.class_room import FindClassRoom
from app.model.class_room.class_room import ClassRoom
from app.model.class_room.class_room import ClassRoomId
from app.model.user.user import User
from app.model.user.user import UserId


class CreateClassRoomTest(TestCase):
    def setUp(self):
        self.class_room_dict = {
            'name': 'test name',
            'image_url': 'https://example.example.com/test.jpg',
            'publish_type': 'private',
            'tag_list': ['tag1', 'tag2'],
            'capacity': 10,
            'caption': 'test caption'
        }
        self.user_dict = {
            'user_id': '79434f7e-b53f-4d3a-8c79-aedc7b73af39',
            'nickname': 'Naoki',
            'user_name': {
                'first_name': '直紀',
                'last_name': '三好'
            },
            'user_name_kana': {
                'first_name_kana': 'ナオキ',
                'last_name_kana': 'ミヨシ'
            },
            'email': 'trombone344@gmail.com',
            'register_date': '2020-02-26T00:18:16.874000+09:00',
            'cognito_user_sub': '79434f7e-b53f-4d3a-8c79-aedc7b73af39'
        }
        self.user = User.from_dict(self.user_dict)

    def test_run(self):
        # datasource の作成
        datasource = MagicMock()
        datasource.fetch_sequesnse_id = MagicMock(return_value=1)
        # user service の作成
        user_service = MagicMock(spec=UserQueryService)
        user_service.find = MagicMock(return_value=self.user)

        usecase = CreateClassRoom(datasource=datasource,
                                  user_service=user_service,
                                  logger=MagicMock())
        user_id = UserId('79434f7e-b53f-4d3a-8c79-aedc7b73af39')
        result = usecase.run(user_id=user_id,
                             item=deepcopy(self.class_room_dict))

        expect = {
            **self.class_room_dict, 'class_room_id':
            1,
            'owner_list': [{
                'user_id': '79434f7e-b53f-4d3a-8c79-aedc7b73af39',
                'nickname': 'Naoki',
                'email': 'trombone344@gmail.com'
            }]
        }
        datasource.fetch_sequesnse_id.assert_called_once()
        datasource.insert_item.assert_called_once_with(
            ClassRoom.from_dict(expect))
        datasource.put_item.assert_not_called()
        user_service.find.assert_called_once_with(user_id)
        self.assertEqual(result.to_dict(), expect)


class FindClassRoomTest(TestCase):
    def setUp(self):
        self.class_room_dict = {
            'class_room_id':
            1,
            'owner_list': [{
                'user_id': '79434f7e-b53f-4d3a-8c79-aedc7b73af39',
                'nickname': 'Naoki-1',
                'email': 'trombone344@gmail.com'
            }, {
                'user_id': '79434f7e-b53f-4d3a-8c79-aedc7b73af39-1',
                'nickname': 'Naoki-1',
                'email': 'trombone344@gmail.com'
            }],
            'name':
            'test name',
            'image_url':
            'https://example.example.com/test.jpg',
            'publish_type':
            'private',
            'tag_list': ['tag1', 'tag2'],
            'capacity':
            10,
            'caption':
            'test caption'
        }

    def test_run_ok(self):
        datasource = MagicMock()
        datasource.find_by_id = MagicMock(
            return_value=ClassRoom.from_dict(self.class_room_dict))
        usecase = FindClassRoom(datasource=datasource, logger=MagicMock())
        result = usecase.run(ClassRoomId(1))

        datasource.find_by_id.assert_called_once_with(ClassRoomId(1))
        self.assertEqual(result.to_dict(), self.class_room_dict)
