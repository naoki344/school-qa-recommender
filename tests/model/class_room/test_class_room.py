from unittest import TestCase

from app.model.class_room.class_room import ClassRoom


class ClassRoomTest(TestCase):
    def test_dict_max(self):
        class_dict = {
            'class_room_id': 1,
            'name': 'test name',
            'image_url': 'https://example.example.com/test.jpg',
            'publish_type': 'private',
            'tag_list': ['tag1', 'tag2'],
            'capacity': 10
        }
        self.assertEqual(ClassRoom.from_dict(class_dict).to_dict(), class_dict)

    def test_dict_min(self):
        class_dict = {
            'class_room_id': 1,
            'name': 'test name',
            'image_url': 'https://example.example.com/test.jpg',
            'publish_type': 'private',
            'tag_list': ['tag1', 'tag2']
        }
        self.assertEqual(
            ClassRoom.from_dict(class_dict).to_dict(), {
                **class_dict, 'capacity': None
            })
