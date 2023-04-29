import unittest
from unittest.mock import MagicMock
from sqlalchemy.orm import Session
from src.database.models import User, Contact
from src.schemas import ContactInputModel
from src.repository.contacts import (

    post_contact,
    get_contacts,
    get_contact,
    put_contact,
    delete_contact,
    search_everywhere_contacts,
    get_birthdays_week,
    filter_contacts
)


class TestContacts(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.user = User(id=1)


    async def test_post_contact(self):
        body = ContactInputModel(name="Test",
                                 surname="Surname",
                                 email="test@email.com",
                                 phone="111222333",
                                 birthday='1990-01-01')

        result = await post_contact(body=body, user=self.user, db=self.session)
        self.assertEqual(result.name, body.name)
        self.assertEqual(result.surname, body.surname)
        self.assertEqual(result.email, body.email)
        self.assertTrue(hasattr(result, "id"))


    async def test_get_contacts(self):
        contacts = [Contact(), ]
        self.session.query().filter().offset().limit().all.return_value = contacts
        result = await get_contacts(skip=0, limit=10, user=self.user, db=self.session)
        self.assertEqual(result, contacts)
        self.assertListEqual(result, contacts)


    async def test_get_contact(self):
        contact = Contact()
        self.session.query().filter().first.return_value = contact
        result = await get_contact(contact_id=1, user=self.user, db=self.session)
        self.assertEqual(result, contact)


    async def test_get_contact_not_found(self):
        self.session.query().filter().first.return_value = None
        result = await get_contact(contact_id=1, user=self.user, db=self.session)
        self.assertIsNone(result)


    async def test_put_contact(self):
        contact = Contact()
        body = ContactInputModel(name="Test",
                                 surname="Surname",
                                 email="test@email.com",
                                 phone="111222333",
                                 birthday='1990-01-01')
        self.session.query().filter().first.return_value = contact
        self.session.commit.return_value = None
        result = await put_contact(contact_id=1, body=body, user=self.user, db=self.session)
        self.assertEqual(result, contact)


    async def test_put_contact_not_found(self):
        body = ContactInputModel(name="Test",
                                 surname="Surname",
                                 email="test@email.com",
                                 phone="111222333",
                                 birthday='1990-01-01')
        self.session.query().filter().first.return_value = None
        self.session.commit.return_value = None
        result = await put_contact(contact_id=1, body=body, user=self.user, db=self.session)
        self.assertIsNone(result)


    async def test_delete_contact(self):
        contact = Contact()
        self.session.query().filter().first.return_value = contact
        result = await delete_contact(contact_id=1,
                                      user=self.user,
                                      db=self.session)
        self.assertEqual(result, contact)


    async def test_delete_contact_not_found(self):
        self.session.query().filter().first.return_value = None

        result = await delete_contact(contact_id=1,
                                      user=self.user,
                                      db=self.session)

        self.assertIsNone(result)


    async def test_search_everywhere_contacts(self):
        contacts = [Contact(), Contact()]
        self.session.query().filter().filter().all.return_value = contacts

        result = await search_everywhere_contacts(parameter='test',
                                                  user=self.user,
                                                  db=self.session)

        self.assertEqual(result, contacts)


    async def test_filter_contacts(self):
        contact = [Contact(), Contact()]
        self.session.query().filter().all.return_value = contact

        result = await filter_contacts(name='Test',
                                       surname='Test',
                                       email='email@com',
                                       user=self.user,
                                       db=self.session)

        self.assertEqual(result, contact)


    async def test_get_birthdays_week(self):
        contacts = []
        self.session.query().filter().all.return_value = contacts

        result = await get_birthdays_week(user=self.user,
                                          db=self.session)

        self.assertEqual(result, contacts)
        self.assertListEqual(result, contacts)


if __name__ == '__main__':
    unittest.main()
