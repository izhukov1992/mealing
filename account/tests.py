from django.test import TestCase
from django.test.client import Client
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from .constants import CLIENT, TRAINER, MODERATOR
from .models import Account


class UserModelTestCase(TestCase):
    def setUp(self):
        user = User.objects.create(username="username_correct")
        user.set_password("password_correct")
        user.save()

    def test_authentication_incorrect_username(self):
        user = User.objects.get(username="username_correct")
        auth = authenticate(username="username_incorrect", password="password_correct")
        self.assertEqual(auth, None)

    def test_authentication_incorrect_password(self):
        user = User.objects.get(username="username_correct")
        auth = authenticate(username="username_correct", password="password_incorrect")
        self.assertEqual(auth, None)

    def test_authentication_incorrect_username_and_password(self):
        user = User.objects.get(username="username_correct")
        auth = authenticate(username="username_incorrect", password="password_incorrect")
        self.assertEqual(auth, None)

    def test_authentication_correct(self):
        user = User.objects.get(username="username_correct")
        auth = authenticate(username="username_correct", password="password_correct")
        self.assertNotEqual(auth, None)


class AccountModelTestCase(TestCase):
    def setUp(self):
        user1 = User.objects.create(username="username1_correct")
        user1.set_password("password1_correct")
        user1.save()
        Account.objects.create(user=user1)
        
        user2 = User.objects.create(username="username2_correct")
        user2.set_password("password2_correct")
        user2.save()
        Account.objects.create(user=user2, limit=1000)
        
        user3 = User.objects.create(username="username3_correct")
        user3.set_password("password3_correct")
        user3.save()
        Account.objects.create(user=user3, role=MODERATOR)

    def test_account_limit_default(self):
        account = Account.objects.get(user=User.objects.get(username="username1_correct"))
        self.assertEqual(account.limit, 2500)

    def test_account_limit_custom(self):
        account = Account.objects.get(user=User.objects.get(username="username2_correct"))
        self.assertEqual(account.limit, 1000)

    def test_account_role_default(self):
        account = Account.objects.get(user=User.objects.get(username="username1_correct"))
        self.assertEqual(account.role, CLIENT)

    def test_account_role_admin(self):
        account = Account.objects.get(user=User.objects.get(username="username3_correct"))
        self.assertEqual(account.role, MODERATOR)


class SignUpAPITestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_signup_incorrect_username_is_empty(self):
        response = self.client.post("/api/v1/user/", '{"username": "", "password": "password_correct", "password_confirm": "password_correct"}', 'application/json')
        self.assertEqual(response.status_code, 400)

    def test_signup_incorrect_password_is_empty(self):
        response = self.client.post("/api/v1/user/", '{"username": "username_correct", "password": "", "password_confirm": "password_correct"}', 'application/json')
        self.assertEqual(response.status_code, 400)

    def test_signup_incorrect_passwords_mismatch(self):
        response = self.client.post("/api/v1/user/", '{"username": "username_correct", "password": "password_correct", "password_confirm": "password_incorrect"}', 'application/json')
        self.assertEqual(response.status_code, 400)

    def test_signup_incorrect_username_in_use(self):
        response = self.client.post("/api/v1/user/", '{"username": "username_correct", "password": "password_correct", "password_confirm": "password_correct"}', 'application/json')
        response = self.client.post("/api/v1/user/", '{"username": "username_correct", "password": "password_correct", "password_confirm": "password_correct"}', 'application/json')
        self.assertEqual(response.status_code, 400)

    def test_signup_correct(self):
        response = self.client.post("/api/v1/user/", '{"username": "username_correct", "password": "password_correct", "password_confirm": "password_correct"}', 'application/json')
        self.assertEqual(response.status_code, 200)
        account = Account.objects.get(user=User.objects.get(username="username_correct"))
        self.assertNotEqual(account, None)


class SignInAPITestCase(TestCase):
    def setUp(self):
        self.client = Client()
        
        user = User.objects.create(username="username_correct")
        user.set_password("password_correct")
        user.save()
        Account.objects.create(user=user)

    def test_signin_incorrect_username_is_empty(self):
        response = self.client.post("/api/v1/auth/", '{"username": "", "password": "password_correct"}', 'application/json')
        self.assertEqual(response.status_code, 400)

    def test_signin_incorrect_password_is_empty(self):
        response = self.client.post("/api/v1/auth/", '{"username": "username_correct", "password": ""}', 'application/json')
        self.assertEqual(response.status_code, 400)

    def test_signin_incorrect_username_incorrect(self):
        response = self.client.post("/api/v1/auth/", '{"username": "username_incorrect", "password": "password_correct"}', 'application/json')
        self.assertEqual(response.status_code, 400)

    def test_signin_incorrect_password_incorrect(self):
        response = self.client.post("/api/v1/auth/", '{"username": "username_correct", "password": "password_incorrect"}', 'application/json')
        self.assertEqual(response.status_code, 400)

    def test_signin_correct(self):
        response = self.client.post("/api/v1/auth/", '{"username": "username_correct", "password": "password_correct"}', 'application/json')
        self.assertEqual(response.status_code, 200)


class SignOutAPITestCase(TestCase):
    def setUp(self):
        self.client = Client()
        
        user = User.objects.create(username="username_correct")
        user.set_password("password_correct")
        user.save()
        Account.objects.create(user=user)

    def test_signout(self):
        response = self.client.post("/api/v1/auth/", '{"username": "username_correct", "password": "password_correct"}', 'application/json')
        self.assertEqual(response.status_code, 200)
        response = self.client.delete("/api/v1/auth/")
        self.assertEqual(response.status_code, 200)


class UserAPITestCase(TestCase):
    def setUp(self):
        self.client = Client()
        user = User.objects.create(username="username_correct")
        user.set_password("password_correct")
        user.is_staff = True		
        user.save()
        account = Account.objects.create(user=user, role=MODERATOR)

    def test_user_crud(self):
        ## post
        response = self.client.post("/api/v1/user/", '{"username": "username1_correct", "password": "password1_correct", "password_confirm": "password1_correct"}', 'application/json')
        self.assertEqual(response.status_code, 200)
        # sign out before new registration
        response = self.client.delete("/api/v1/auth/")
        self.assertEqual(response.status_code, 200)
        response = self.client.post("/api/v1/user/", '{"username": "username2_correct", "password": "password2_correct", "password_confirm": "password2_correct"}', 'application/json')
        self.assertEqual(response.status_code, 200)
        
        ## get
        response = self.client.get("/api/v1/user/")
        self.assertEqual(response.status_code, 200)
        # permissions only to own user instance
        response = self.client.get("/api/v1/user/1/")
        self.assertEqual(response.status_code, 404)
        response = self.client.get("/api/v1/user/2/")
        self.assertEqual(response.status_code, 404)
        response = self.client.get("/api/v1/user/3/")
        self.assertEqual(response.status_code, 200)
        
        response = self.client.get("/api/v1/account/")
        self.assertEqual(response.status_code, 200)
        # permissions only to own account instance
        response = self.client.get("/api/v1/account/1/")
        self.assertEqual(response.status_code, 404)
        response = self.client.get("/api/v1/account/2/")
        self.assertEqual(response.status_code, 404)
        response = self.client.get("/api/v1/account/3/")
        self.assertEqual(response.status_code, 200)
        
        # sign in as admin
        response = self.client.delete("/api/v1/auth/")
        self.assertEqual(response.status_code, 200)
        response = self.client.post("/api/v1/auth/", '{"username": "username_correct", "password": "password_correct"}', 'application/json')
        self.assertEqual(response.status_code, 200)
        
        # try get again
        response = self.client.get("/api/v1/user/1/")
        self.assertEqual(response.status_code, 200)
        response = self.client.get("/api/v1/user/2/")
        self.assertEqual(response.status_code, 200)
        response = self.client.get("/api/v1/account/1/")
        self.assertEqual(response.status_code, 200)
        response = self.client.get("/api/v1/account/2/")
        self.assertEqual(response.status_code, 200)
        
        ## update
        user = User.objects.get(username="username2_correct")
        account = Account.objects.get(user=user)
        self.assertEqual(user.email, "")
        self.assertEqual(account.role, CLIENT)
        self.assertEqual(account.limit, 2500)
        
        response = self.client.put("/api/v1/user/3/", '{"username": "username2_correct", "password": "password2_correct", "email": "user@user.com", "role": "Trainer"}', 'application/json')
        self.assertEqual(response.status_code, 200)
        response = self.client.put("/api/v1/account/3/", '{"limit": 1000}', 'application/json')
        self.assertEqual(response.status_code, 200)
        
        user = User.objects.get(username="username2_correct")
        account = Account.objects.get(user=user)
        self.assertEqual(user.email, "user@user.com")
        self.assertEqual(account.role, TRAINER)
        self.assertEqual(account.limit, 1000)
        
        ## delete
        response = self.client.delete("/api/v1/user/2/")
        self.assertEqual(response.status_code, 204)
