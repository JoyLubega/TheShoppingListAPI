import unittest
from flask import json
from api import db
from api.shoppinglistApi import app
from instance.config import application_config


class ItemTestCase(unittest.TestCase):
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

    def test_add_item_with_no_name(self):
        """Should return 400 for missing item name"""
        item = json.dumps({'item': ''})
        response = self.client.post('/shoppinglists/1/items', data=item,
                                    headers={"Authorization": self.token})
        self.assertEqual(response.status_code, 200)
        self.assertIn('Missing Item name', response.data.decode())

    def test_add_item_when_shoppinglist_doesnt_exist(self):
        """Should return 400 for missing shoppinglist"""
        item = json.dumps({'item': 'Going to Kenya'})
        response = self.client.post('/shoppinglists/1/items', data=item,
                                    headers={"Authorization": self.token})
        self.assertEqual(response.status_code, 200)
        self.assertIn('shoppinglist with id 1 not found', response.data.decode())

    def test_add_item_successfully(self):
        """Should return 201 for item added"""

        # First add the shoppinglist
        shoppinglist = json.dumps({
            'shoppinglist': 'Travel to china',
            'desc': 'Vaction'
        })
        self.client.post('/shoppinglists', data=shoppinglist,
                         headers={"Authorization": self.token})

        item = json.dumps({
            'item': 'Go to Kenya',
            'status' : "false"
        })
        response = self.client.post('/shoppinglists/1/items', data=item,
                                    headers={"Authorization": self.token})
        self.assertEqual(response.status_code, 201)
        self.assertIn('Go to Kenya', response.data.decode())

    def test_get_items_when_DB_empty(self):
        """Should return no items msg"""

        response = self.client.get('/items/1',
                                   headers={"Authorization": self.token})
        self.assertEqual(response.status_code, 200)
        

    def test_get_items(self):
        """Should return all  items"""

        # First add item
        self.test_add_item_successfully()
        response = self.client.get('/items/1',
                                   headers={"Authorization": self.token})
        self.assertEqual(response.status_code, 200)
        self.assertIn('Go to kenya',
                      response.data.decode())

    def test_add_duplicate_item(self):
        """Should return 409 for duplicate item"""

        # First add the item
        self.test_add_item_successfully()
        item = json.dumps({'item': 'Go to Kenya'})
        response = self.client.post('/shoppinglists/1/items', data=item,
                                    headers={"Authorization": self.token})
        self.assertEqual(response.status_code, 409)
        self.assertIn('item name Already exists', response.data.decode())

    def test_edit_item_with_no_name(self):
        """Should return 400 for missing item name"""

        item = json.dumps({
            'item': '',
            'status': ''
        })
        response = self.client.put('/shoppinglists/1/items/1', data=item,
                                   headers={"Authorization": self.token})
        self.assertEqual(response.status_code, 200)
        self.assertIn('Missing parameters', response.data.decode())

    def test_edit_item_with_missing_shoppinglist(self):
        """Should return 400 for missing shoppinglist"""

        item = json.dumps({
            'item': 'Go to New York',
            'status': "false"
        })
        response = self.client.put('/shoppinglists/1/items/1', data=item,
                                   headers={"Authorization": self.token})
        self.assertEqual(response.status_code, 200)
        self.assertIn('shoppinglist with id 1 not found', response.data.decode())

    def test_edit_item_with_missing_item(self):
        """Should return 400 for missing item"""

        # First add the 
        shoppinglist= json.dumps({
            'shoppinglist': 'Travel',
            'desc': 'Visit places'
        })
        self.client.post('/shoppinglists', data=shoppinglist,
                         headers={"Authorization": self.token})
        item = json.dumps({
            'item': 'Go to New York',
            'status': "false"
        })
        response = self.client.put('/shoppinglists/1/items/1', data=item,
                                   headers={"Authorization": self.token})
        self.assertEqual(response.status_code, 200)
        self.assertIn('item with id 1 does not exist',
                      response.data.decode())

    def test_edit_item_with_invalid_status(self):
        """Should return 201 for item edited"""

        self.test_add_item_successfully()
        item = json.dumps({
            'item': 'Go to Silicon Valley',
            'status': "hello"
        })
        response = self.client.put('/shoppinglists/1/items/1', data=item,
                                   headers={"Authorization": self.token})
        self.assertEqual(response.status_code, 409)
        self.assertIn('status should be true or false', response.data.decode())

    def test_edit_item_succesfully(self):
        """Should return 201 for item edited"""

        self.test_add_item_successfully()
        item = json.dumps({
            'item': 'Go to Silicon Valley',
            'status': "false"
        })
        response = self.client.put('/shoppinglists/1/items/1', data=item,
                                   headers={"Authorization": self.token})
        self.assertEqual(response.status_code, 201)
        self.assertIn('Go to Silicon Valley', response.data.decode())

    def test_delete_item_that_doesnt_exist(self):
        """Should return 400 for missing item"""

        response = self.client.delete('/items/1',
                                      headers={"Authorization": self.token})
        self.assertEqual(response.status_code, 200)
        self.assertIn('Item with id 1 does not exist', response.data.decode())

    def test_delete_item_successfully(self):
        """Should return 201 for item deleted"""

        self.test_add_item_successfully()
        response = self.client.delete('/items/1',
                                      headers={"Authorization": self.token})
        self.assertEqual(response.status_code, 201)
        self.assertIn('Item deleted', response.data.decode())

    def tearDown(self):
        # Drop all tables
        with app.app_context():
            # Drop all tables
            db.session.remove()
            db.drop_all()


if __name__ == '__main__':
    unittest.main()