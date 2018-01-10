from flask import jsonify
from models.models import ShoppinglistModel, ItemModel


class Item(object):
    """
    Handles all item operations
    """

    @staticmethod
    def get_items(shoppinglist_id):
        """
        Gets all items
        :param shoppinglist_id:
        :return:
        """
        response = ItemModel.query.all()
        if not response:
            response = jsonify({"Error":"No items"})
            response.status_code = 400
            return response
        else:
            res = [item for item in
                   response if item.shoppinglist_id == shoppinglist_id]
            item_data = []
            for data in res:
                final = {
                    'id': data.id,
                    'name': data.name,
                    'status': data.status,
                    'date_added': data.date_added,
                    'shoppinglist_id' : data.shoppinglist_id
                }
                item_data.append(final)
            response = jsonify(item_data)
            response.status_code = 200
            return response

    


    @staticmethod
    def add_item(user_id, shoppinglist_id, item_name):
        """
        Adds an item
        :param user_id:
        :param shoppinglist_id:
        :param item_name:
        """
        if not item_name:
            response = jsonify({'Error': 'Missing Item name'})
            response.status_code = 404
            return response

        # if not item_name.isalpha():
        #     response = jsonify({'Error': 'Names must be in alphabetical strings'})
        #     response.status_code = 400
        #     return response

        shoppinglist = ShoppinglistModel.query.filter_by(id=shoppinglist_id,
                                             user_id=user_id).first()
        if not shoppinglist:
            response = jsonify({'Error': 'Shoppinglist with id '
                                         + str(user_id) + ' not found'})
            response.status_code = 404
            return response

        item = ItemModel(name=item_name, shoppinglist_id=shoppinglist_id)
        try:
            item.save()
            response = jsonify({
                'id': item.id,
                'name': item.name,
                'status': item.status,
                'date_added': item.date_added,
                'shoppinglist_id': shoppinglist_id
            })
            response.status_code = 201
            return response
        except Exception:
            response = jsonify({'Error': 'item name Already exists'})
            response.status_code = 409
            return response

    @staticmethod
    def edit_item(user_id, shoppinglist_id, item_id, new_item_name ):
        """
        Edits an item
        :param user_id:
        :param shoppinglist_id:
        :param item_id:
        :param new_item_name:
        :param new_item_status:
        """
        if not new_item_name: 
            response = jsonify({'Error': 'Missing parameters'})
            response.status_code = 404
            return response

        # allowed_status = ["true", "false"]
        # if new_item_status not in allowed_status:
        #     response = jsonify({'Error': 'status should be true or false'})
        #     response.status_code = 409
        #     return response

        shoppinglist = ShoppinglistModel.query.filter_by(id=shoppinglist_id,
                                             user_id=user_id).first()
        if not shoppinglist:
            response = jsonify({'Error': 'Shoppinglist with  that id doesnt exist '})
            response.status_code = 404
            return response



        item = ItemModel.query.filter_by(shoppinglist_id=shoppinglist_id).filter_by(id=item_id).first()
        if not item:
            response = jsonify({
                'Error': 'item with id ' + str(item_id) + ' does not exist'
            })
            response.status_code = 404
            return response

        item.name = new_item_name
        #item.status = new_item_status
        try:
            item.save()
            response = jsonify({
                'id': item.id,
                'name': item.name,
                #'status': item.status,
                'date_added': item.date_added,
                'shoppinglist_id': shoppinglist_id
            })
            response.status_code = 201
            return response
        except Exception:
            response = jsonify({'Error': 'Item name Already exists'})
            response.status_code = 409
            return response

    @staticmethod
    def delete_item(item_id):
        """
        Deletes an item
        :param item_id:
        """
        item = ItemModel.query.filter_by(id=item_id).first()
        if not item:
            response = jsonify({
                'Error': 'Item with id '
                         + str(item_id) + ' does not exist '
            })
            response.status_code = 404
            return response

        item.delete()
        response = jsonify({
            'success': 'Item deleted'
        })
        response.status_code = 200
        return response