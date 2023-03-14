import sys
import os
from datetime import date, datetime
sys.path.append(os.getcwd())

import unittest
from unittest.mock import MagicMock

from sqlalchemy.orm import Session

from src.database.models import Contact, User
from src.schemas import ContactModel, ContactUpdate
from src.repository.contacts import (
    get_contacts,
    get_contact,
    get_contacts_by_fname,
    get_contacts_by_lname,
    get_contacts_by_email,
    get_contacts_by_birthday,
    create_contact,
    update_contact,
    remove_contact
)


class TestContacts(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.user = User(id=1)
    
    # get contacts test
    async def test_get_contacts(self):
        contacts = [Contact(), Contact(), Contact()]
        self.session.query().filter().offset().limit().all.return_value = contacts
        result = await get_contacts(skip=0, limit=10, user=self.user, db=self.session)
        self.assertEqual(result, contacts)

    # get contact test
    async def test_get_contact_found(self):
        contact = Contact()
        self.session.query().filter().first.return_value = contact
        result = await get_contact(contact_id=1, user=self.user, db=self.session)
        self.assertEqual(result, contact)

    async def test_get_contact_not_found(self):
        self.session.query().filter().first.return_value = None
        result = await get_contact(contact_id=1, user=self.user, db=self.session)
        self.assertIsNone(result)
    
    # get contact by first_name test
    async def test_get_contact_by_fname_found(self):
        contacts = [Contact(), Contact(), Contact()]
        self.session.query().filter().all.return_value = contacts
        result = await get_contacts_by_fname(first_name="art", user=self.user, db=self.session)
        self.assertEqual(result, contacts)
        
    async def test_get_contact_by_fname_not_found(self):
        self.session.query().filter().all.return_value = None
        result = await get_contacts_by_fname(first_name="art", user=self.user, db=self.session)
        self.assertIsNone(result)
    
    # get contact by last_name test
    async def test_get_contact_by_lname_found(self):
        contacts = [Contact(), Contact(), Contact()]
        self.session.query().filter().all.return_value = contacts
        result = await get_contacts_by_lname(last_name="enko", user=self.user, db=self.session)
        self.assertEqual(result, contacts)
        
    async def test_get_contact_by_lname_not_found(self):
        self.session.query().filter().all.return_value = None
        result = await get_contacts_by_lname(last_name="enko", user=self.user, db=self.session)
        self.assertIsNone(result)
    
    # get contact by email test
    async def test_get_contact_by_email_found(self):
        contacts = [Contact(), Contact(), Contact()]
        self.session.query().filter().all.return_value = contacts
        result = await get_contacts_by_email(email="gmail", user=self.user, db=self.session)
        self.assertEqual(result, contacts)
        
    async def test_get_contact_by_fname_not_found(self):
        self.session.query().filter().all.return_value = None
        result = await get_contacts_by_email(email="gmail", user=self.user, db=self.session)
        self.assertIsNone(result)
    
    #  get contact by bitrhday test
    async def test_get_contact_by_byrthday_found(self):
        contacts = [Contact(birthday=date(2000, 3, 15))]
        self.session.query().filter().all.return_value = contacts
        result = await get_contacts_by_birthday(user=self.user, db=self.session)
        self.assertEqual(result, contacts)
        
    async def test_get_contact_by_byrthday_not_found(self):
        contacts = []
        self.session.query().filter().all.return_value = contacts
        result = await get_contacts_by_birthday(user=self.user, db=self.session)
        self.assertEqual(result, contacts)
        
    # create contact test
    async def test_create_contact(self):
        body = ContactModel(
            first_name="Cristiano",
            last_name="Ronaldo",
            email="cr7@gmail.com",
            phone="123123123",
            birthday=date(2003, 2, 3)
        )
        result = await create_contact(body=body, user=self.user, db=self.session)
        self.assertEqual(result.first_name, body.first_name)
        self.assertEqual(result.last_name, body.last_name)
        self.assertEqual(result.email, body.email)
        self.assertEqual(result.phone, body.phone)
        self.assertEqual(result.birthday, body.birthday)
        self.assertTrue(hasattr(result, "id"))
    
    # remove contact test
    async def test_remove_contact_found(self):
        contact = Contact()
        self.session.query().filter().first.return_value = contact
        result = await remove_contact(contact_id=1, user=self.user, db=self.session)
        self.assertEqual(result, contact)

    async def test_remove_contact_not_found(self):
        self.session.query().filter().first.return_value = None
        result = await remove_contact(contact_id=1, user=self.user, db=self.session)
        self.assertIsNone(result)

    # update contact test
    async def test_update_contact_found(self):
        body = ContactUpdate(
            first_name="Cristiano",
            last_name="Ronaldo",
            email="cr7@gmail.com",
            phone="123123123",
            birthday=date(2003, 2, 3)
        )
        contact = ContactModel(
            first_name="Artur",
            last_name="Ronaldo",
            email="cr7@gmail.com",
            phone="123123123",
            birthday=date(2000, 2, 3)
        )
        self.session.query().filter().first.return_value = contact
        self.session.commit.return_value = None
        result = await update_contact(contact_id=1, body=body, user=self.user, db=self.session)
        self.assertEqual(result, contact)

    async def test_update_contact_not_found(self):
        body = ContactUpdate(
            first_name="Cristiano",
            last_name="Ronaldo",
            email="cr7@gmail.com",
            phone="123123123",
            birthday=date(2003, 2, 3)
        )
        self.session.query().filter().first.return_value = None
        self.session.commit.return_value = None
        result = await update_contact(contact_id=1, body=body, user=self.user, db=self.session)
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()
