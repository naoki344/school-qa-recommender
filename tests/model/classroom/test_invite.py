from unittest import TestCase
import uuid
import freezegun

from app.model.classroom.invite import ClassmateInvite
from app.model.classroom.classroom import ClassroomId


class ClassmateInviteTest(TestCase):
    def setUp(self):
        self.maxDiff = None
        self.invite_dict = {
            'classroom_id': 1,
            'invite_key': str(uuid.uuid4()),
            'expire_date': '2020-02-15T00:18:16.874000+09:00'
        }

    @freezegun.freeze_time('2020-02-01T00:18:16.874000+09:00')
    def test_create(self):
        invite = ClassmateInvite.create(
            classroom_id=ClassroomId(1))
        self.assertEqual(
            type(invite.invite_key.value), str)
        self.assertEqual(
            invite.classroom_id.value, 1)
        self.assertEqual(
            invite.expire_date.to_string(),
            '2020-02-15T00:18:16.874000+09:00')

    def test_dict(self):
        invite = ClassmateInvite.from_dict(
                self.invite_dict)
        self.assertEqual(
            invite.to_dict(), self.invite_dict)
