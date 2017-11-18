import unittest
from flask import json
from api import db
from api.shoppinglistApi import app
from instance.config import application_config


class AuthenticationTestCase(unittest.TestCase):
    def setUp(self):
        app.config.from_object(application_config['TestingEnv'])
        self.client = app.test_client()

        # Binds the app to current context
        with app.app_context():
            # Create all tables
            db.create_all()

    def test_index_route(self):
        response = self.client.get('/')
        self.assertIn('Welcome to the Shoppinglist API', response.data.decode())

    def test_registration_with_missing_credentials(self):
        """Should throw error for missing credentials"""
        user = json.dumps({
            'name': '',
            'email': '',
            'password': ''
        })
        response = self.client.post('/auth/register', data=user)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Missing', response.data.decode())

    def test_registration_with_invalid_email(self):
        """Should return invalid email"""
        user = json.dumps({
            'name': 'joyce',
            'email': 'jo',
            'password': 'lubega'
        })
        response = self.client.post('/auth/register', data=user)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Invalid Email', response.data.decode())

    def test_registration_with_short_password(self):
        """Should return invalid email"""
        user = json.dumps({
            'name': 'joyce',
            'email': 'joyce@gmail.com',
            'password': 'lub'
        })
        response = self.client.post('/auth/register', data=user)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Password is short', response.data.decode())

    def test_for_existing_email(self):
        """Should check if email exists"""
        user = json.dumps({
            'name': 'joyce',
            'email': 'joyce@gmail.com',
            'password': 'gracelubega'
        })
        self.client.post('/auth/register', data=user)
        response = self.client.post('/auth/register', data=user)
        self.assertEqual(response.status_code, 401)
        self.assertIn('Email Already exists', response.data.decode())

    def test_successfull_registration(self):
        """Should register user successfully"""
        user = json.dumps({
            'name': 'joyce',
            'email': 'joyce@gmail.com',
            'password': 'lubegagrace'
        })
        response = self.client.post('/auth/register', data=user)
        self.assertEqual(response.status_code, 201)
        self.assertIn('Successfully registered', response.data.decode())

    def test_login_without_credentials(self):
        """Should check for valid email"""
        user = json.dumps({
            'email': '',
            'password': ''
        })
        response = self.client.post('/auth/login', data=user)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Missing login credentials', response.data.decode())

    def test_login_with_invalid_email(self):
        """Should check for valid email"""
        user = json.dumps({
            'email': 'joyce',
            'password': 'lubegagrace'
        })
        response = self.client.post('/auth/login', data=user)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Enter valid email', response.data.decode())

    def test_incorrect_login_credentials(self):
        """Should check for valid email"""

        # First of all register
        self.test_successfull_registration()
        user = json.dumps({
            'email': 'incorrect@gmail.com',
            'password': 'incorrect'
        })
        response = self.client.post('/auth/login', data=user)
        self.assertEqual(response.status_code, 401)
        self.assertIn('Incorrect email or password', response.data.decode())

    def test_successful_login(self):
        """Should check for valid email"""

        # First of all register
        self.test_successfull_registration()
        user = json.dumps({
            'email': 'joyce@gmail.com',
            'password': 'lubegagrace'
        })
        response = self.client.post('/auth/login', data=user)
        self.assertEqual(response.status_code, 201)
        self.assertIn('Login Successful', response.data.decode())

    def test_reset_password_with_no_password(self):
        """Should throe error for non existing email"""

        # First of all register
        self.test_successfull_registration()
        user = json.dumps({
            'email': 'joelosten@gmail.com',
            'old_password': '',
            'new_password': ''
        })
        response = self.client.post('/auth/reset-password', data=user)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Missing email or password', response.data.decode())

    def test_reset_password_for_non_exisiting_email(self):
        """Should throe error for non existing email"""

        # First of all register
        self.test_successfull_registration()
        user = json.dumps({
            'email': 'andela@gmail.com',
            'old_password': 'secret',
            'new_password': 'qwerty'
        })
        response = self.client.post('/auth/reset-password', data=user)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Email and password does not exist', response.data.decode())

    def test_reset_password_with_wrong_password(self):
        """Should throw 400 error for wrong password"""

        # First of all register
        self.test_successfull_registration()
        user = json.dumps({
            'email': 'andela@gmail.com',
            'old_password': 'secret4',
            'new_password': 'secret3'
        })
        response = self.client.post('/auth/reset-password', data=user)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Email and password does not exist', response.data.decode())

    def test_reset_password_successfully(self):
        """Should throw 400 error for wrong password"""

        # First of all register
        self.test_successfull_registration()
        user = json.dumps({
            'email': 'joyce@gmail.com',
            'old_password': 'lubegagrace',
            'new_password': 'akansaseve'
        })
        response = self.client.post('/auth/reset-password', data=user)
        self.assertEqual(response.status_code, 200)
        self.assertIn('password updated', response.data.decode())

    def tearDown(self):
        # Drop all tables
        with app.app_context():
            # Drop all tables
            db.session.remove()
            db.drop_all()


if __name__ == '__main__':
    unittest.main()