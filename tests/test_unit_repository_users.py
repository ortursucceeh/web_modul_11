import sys
import os
from datetime import date, datetime
sys.path.append(os.getcwd())

import unittest
from unittest.mock import MagicMock

from sqlalchemy.orm import Session

from src.database.models import User
from src.schemas import UserModel
from src.repository.users import (
    get_user_by_email,
    create_user,
    update_token,
    confirmed_email,
    update_avatar,
)


class TestUsers(unittest.IsolatedAsyncioTestCase):
    
    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.body = UserModel(
            username="debik",
            email="debik228@gmail.com",
            password="123456"
        )
    
    # get user by email test
    async def test_get_user_by_email(self):
        user = User()
        self.session.query().filter().first.return_value = user
        result = await get_user_by_email(email="test1222gmail.com", db=self.session)
        self.assertEqual(result, user)
        
    # get user by email test
    async def test_create_user(self):
        body = self.body
        result = await create_user(body=body, db=self.session)
        self.assertEqual(result.username, body.username)
        self.assertEqual(result.email, body.email)
        self.assertEqual(result.password, body.password)
        self.assertTrue(hasattr(result, "id"))
        

    # get user by email test
    async def test_confirmed_email(self):
        body = self.body
        await create_user(body=body, db=self.session)
        await confirmed_email(email=body.email, db=self.session)
        result = await get_user_by_email(email=body.email, db=self.session)
        self.assertEqual(result.confirmed, True)

if __name__ == '__main__':
    unittest.main()

