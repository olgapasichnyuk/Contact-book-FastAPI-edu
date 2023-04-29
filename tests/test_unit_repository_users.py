import unittest
from unittest.mock import MagicMock

from sqlalchemy.orm import Session

from src.database.models import User
from src.schemas import UserModel
from src.repository.users import (
    get_user_by_email,
    create_user, update_token, update_avatar, mark_email_confirmed, )


class TestUsers(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.session = MagicMock(spec=Session)

    async def test_get_user_by_email(self):
        user = User()
        self.session.query().filter().first.return_value = user

        result = await get_user_by_email(email='testuser@example.com',
                                         db=self.session)

        self.assertEqual(result, user)

    async def test_get_user_by_email_not_found(self):
        self.session.query().filter().first.return_value = None

        result = await get_user_by_email(email='testuser@example.com',
                                         db=self.session)

        self.assertIsNone(result)

    async def test_create_user(self):
        body = UserModel(username='Testuser', email='testuser@example.com', password='12345678')

        result = await create_user(body=body, db=self.session)
        self.assertEqual(result.username, body.username)
        self.assertEqual(result.email, body.email)
        self.assertEqual(result.password, body.password)
        self.assertTrue(hasattr(result, "id"))

    async def test_update_token(self):
        result = await update_token(user=User(), token='123', db=self.session)
        self.assertIsNone(result)

    async def test_mark_email_confirmed(self):
        result = await mark_email_confirmed(email='testuser@example.com',
                                            db=self.session)

        self.assertIsNone(result)

    async def test_update_avatar(self):
        user = User()
        self.session.query().filter().first.return_value = user
        result = await update_avatar(email='testuser@example.com',
                                     url='some_url',
                                     db=self.session)

        self.assertEqual(result, user)


if __name__ == '__main__':
    unittest.main()
