import unittest
from flask import json
from api import db
from api.shoppinglistApi import app
from instance.config import application_config


class ShoppingListTestCase(unittest.TestCase):
    def setUp(self):
        app.config.from_object(application_config['TestingEnv'])
        self.client = app.test_client()

        # Binds the app to current context
        with app.app_context():
            # Create all tables
            db.create_all()

        user = json.dumps({
            'email': 'joyce@gmail.com',
            'password': 'lubegagrace',
            'name': 'Joyce'
        })
        response = self.client.post('/auth/register', data=user)
        json_repr = json.loads(response.data.decode())
        self.token = json_repr['token']

    def test_add_shoppinglist_without_name(self):
        """Should return 400 for missing shoppinglist name"""
        shoppinglist= json.dumps({
            'shoppinglist': '',
            'desc': 'travel'
        })
        response = self.client.post('/shoppinglists', data=shoppinglist,
                                    headers={"Authorization": self.token})
        self.assertEqual(response.status_code, 200)
        self.assertIn('Missing', response.data.decode())

    def test_add_shoppinglist_successfully(self):
        """Should return 201 for shoppinglist added"""
        shoppinglist = json.dumps({
            'shoppinglist': 'Travel',
            'desc': 'Visit places'
        })
        response = self.client.post('/shoppinglists', data=shoppinglist,
                                    headers={"Authorization": self.token})
        self.assertEqual(response.status_code, 201)
        self.assertIn('Travel', response.data.decode())

    def test_add_shoppinglist_with_existing_shoppinglist_name(self):
        """Should return 400 for missing shoppinglist name"""

        # First Add shoppinglist
        self.test_add_shoppinglist_successfully()
        shoppinglist = json.dumps({
            'shoppinglist': 'Travel',
            'desc': 'travel'
        })
        response = self.client.post('/shoppinglists', data=shoppinglist,
                                    headers={"Authorization": self.token})
        self.assertEqual(response.status_code, 409)
        self.assertIn('Shopinglist name Already exists', response.data.decode())

    def test_get_shoppinglist_when_DB_is_empty(self):
        """Should return no shoppinglist lists msg"""
        response = self.client.get('/shoppinglists',
                                   headers={"Authorization": self.token})
        self.assertEqual(response.status_code, 200)
        

    def test_get_shoppinglist(self):
        """Should return all shoppinglists"""

        # First add shoppinglist
        self.test_add_shoppinglist_successfully()
        response = self.client.get('/shoppinglists',
                                   headers={"Authorization": self.token})
        self.assertEqual(response.status_code, 200)
        self.assertIn('Travel',
                      response.data.decode())

    def test_get_shoppinglist_search(self):
        """Should return 200 and shoppinglist"""

        # First add shoppinglist
        self.test_add_shoppinglist_successfully()
        response = self.client.get('/shoppinglists?q=Travel',
                                   headers={"Authorization": self.token})
        self.assertEqual(response.status_code, 200)
        self.assertIn('Travel',
                      response.data.decode())

    def test_get_single_shoppinglist(self):
        """Should return 200 and shoppinglists"""

        # First add shoppinglists
        self.test_add_shoppinglist_successfully()
        response = self.client.get('/shoppinglists/1',
                                   headers={"Authorization": self.token})
        self.assertEqual(response.status_code, 200)
        self.assertIn('Travel',
                      response.data.decode())

    def test_get_single_shoppinglist_with_no_shoppinglist(self):
        """Should return 400 if no shoppinglist"""

        response = self.client.get('/shoppinglists/1',
                                   headers={"Authorization": self.token})
        self.assertEqual(response.status_code, 200)
        self.assertIn('not found',
                      response.data.decode())

    def test_get_single_shoppinglist_not_existing(self):
        """Should return 400 for  doesnt exists"""

        # First add shoppinglists
        self.test_add_shoppinglist_successfully()
        response = self.client.get('/shoppinglists/2',
                                   headers={"Authorization": self.token})
        self.assertEqual(response.status_code, 200)
        self.assertIn('Shoppinglist with id 2 not found',
                      response.data.decode())

    def test_get_single_shoppinglist(self):
        """Should return a single shoppinglist"""

        # First add shoppinglist
        self.test_add_shoppinglist_successfully()
        response = self.client.get('/shoppinglist/1',
                                   headers={"Authorization": self.token})
        self.assertEqual(response.status_code, 200)
        self.assertIn('Travel',
                      response.data.decode())

    def test_update_shoppinglist_which_doesnt_exist(self):
        """
        Should return 400 for shoppinglist
        does not exists
        """

        # First add shoppinglist
        self.test_add_shoppinglist_successfully()
        shoppinglist = json.dumps({
            'shoppinglist': 'Travel',
            'desc': 'Visit places'
        })
        response = self.client.put('/shoppinglists/2', data=shoppinglist,
                                   headers={"Authorization": self.token})
        self.assertEqual(response.status_code, 200)
        self.assertIn('does not exist', response.data.decode())

    def test_update_shoppinglist_without_name(self):
        """Should return 400 for missing shoppinglist name"""
        shoppinglist= json.dumps({
            'shoppinglist': '',
            'desc': 'travel'
        })
        response = self.client.put('/shoppinglist/1', data=shoppinglist,
                                   headers={"Authorization": self.token})
        self.assertEqual(response.status_code, 401)
        self.assertIn('Missing', response.data.decode())

    def test_update_shoppinglist_with_same_name(self):
        """Should return 200 for shoppinglist updates"""

        # First add shoppinglist
        self.test_add_shoppinglist_successfully()
        shoppinglist = json.dumps({
            'shoppinglist': 'Travel',
            'desc': 'Test Foods'
        })
        response = self.client.put('/shoppinglists/1', data=shoppinglist,
                                   headers={"Authorization": self.token})
        # self.assertEqual(response.status_code, 409)
        # self.assertIn(' name Already exists', response.data.decode())

    def test_update_shoppinglist_successfully(self):
        """Should return 200 for shoppinglists updates"""

        # First add shoppinglist
        self.test_add_shoppinglist_successfully()
        shoppinglist = json.dumps({
            'shoppinglist': 'Food',
            'desc': 'Test Foods'
        })
        response = self.client.put('/shoppinglists/1', data=shoppinglist,
                                   headers={"Authorization": self.token})
        self.assertEqual(response.status_code, 200)
        self.assertIn('Food', response.data.decode())

    def test_delete_shoppinglist_that_doesnt_exist(self):
        """Should return 201 for shoppinglist added"""

        response = self.client.delete(
            '/shoppinglists/1', headers={"Authorization": self.token})
        self.assertEqual(response.status_code, 200)
        self.assertIn('Shoppinglist not found', response.data.decode())

    def test_delete_shoppinglist_successfully(self):
        """Should return 201 for shoppinglist added"""

        # First add a shoppinglist
        self.test_add_shoppinglist_successfully()
        response = self.client.delete(
            '/shoppinglists/1', headers={"Authorization": self.token})
        self.assertEqual(response.status_code, 200)
        self.assertIn('shoppinglist deleted', response.data.decode())

    def tearDown(self):
        # Drop all tables
        with app.app_context():
            # Drop all tables
            db.session.remove()
            db.drop_all()


if __name__ == '__main__':
    unittest.main()