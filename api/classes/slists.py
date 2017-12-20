from flask import jsonify,url_for
from flask import request
from models.models import ShoppinglistModel, ItemModel

class ShoppingList(object):
    """
    Handles all shoppinglist operations
    """

    @staticmethod
    def create_shoppinglist(name, desc, user_id):
        """
        Creates a new shoppinglist
        :param name: 
        :param desc: 
        :param user_id: 
        :return: 
        """
        if not name:
            response = jsonify({'Error': 'Missing name'})
            response.status_code = 400
            return response

        if not name.isalpha():
            response = jsonify({'Error': 'Names must be in alphabetical strings'})
            response.status_code = 400
            return response

        shoppinglist = ShoppinglistModel(name=name, desc=desc, user_id=user_id)
        try:
            shoppinglist.save()
            response = jsonify({
                'id': shoppinglist.id,
                'name': shoppinglist.name,
                'desc': shoppinglist.desc,
                'date_added': shoppinglist.date_added,
                'user_id': shoppinglist.user_id
                
            })
            response.status_code = 201
            return response
        except Exception:
            response = jsonify({'Error': 'Shoppinglist name Already exists'})
            response.status_code = 409
            return response

    @staticmethod
    def get_shoppinglists( user_id,search, limit):
        """
        Gets all shoppinglists
        :param user_id: 
        :param search: 
        :return: 
        """
        page = request.args.get('page', 1, type=int)
        #shoppinglist = ShoppinglistModel(name=name,desc=desc, user_id=user_id)
        response = ShoppinglistModel.query.filter_by(user_id=user_id).limit(limit).all()
        if not response:
            response = jsonify([])
            response.status_code = 200
            return response
        else:
            results = []
            
            if search:
                shopping_lists = ShoppinglistModel.query.filter_by(
                    user_id=user_id).filter(ShoppinglistModel.name.like('%{0}%'.format(search)))
            else:
                shopping_lists = ShoppinglistModel.query.filter_by(user_id=user_id)
            
            if shopping_lists:
                pagination = shopping_lists.paginate(page, per_page=limit, error_out=False)
                shop_lists = pagination.items
                if pagination.has_prev:
                    prev = url_for('get_shoppinglists', page=page-1, limit= limit, _external=True)
                else:
                    prev = None
                if pagination.has_next:
                    next = url_for('get_shoppinglists', page=page+1, limit=limit, _external=True)
                else:
                    next = None
                if shop_lists:
                    for shoppinglist in shop_lists:
                        obj = {
                            'id': shoppinglist.id,
                            'name': shoppinglist.name,
                            'desc':shoppinglist.desc
                            }
                        results.append(obj)
                    response = jsonify({
                        'shoppinglists': results,
                        'prev': prev,
                        'next': next,
                        'count': pagination.total
                        })
                    response.status_code = 200
                    return response
                else:
                    return {'message':'No shopping lists to display'}, 404      


        # response = ShoppinglistModel.query.filter_by(user_id=user_id).limit(limit).all()
        # if not response:
        #     response = jsonify([])
        #     response.status_code = 200
        #     return response
        # else:
        #     if search:
        #         res = [shoppinglist for shoppinglist in response if shoppinglist.name
        #                in search and shoppinglist.user_id == user_id]
        #         if not res:
        #             response = jsonify({
        #                 'error': 'The shoppinglist you searched does not exist'
        #             })
        #             return response
        #         else:
        #             shoppinglist_data = []
        #             for data in res:
        #                 final = {
        #                     'id': data.id,
        #                     'name': data.name,
        #                     'desc': data.desc,
        #                     'date_added': data.date_added,
        #                     'user_id': data.user_id
                            
        #                 }
        #                 shoppinglist_data.clear()
        #                 shoppinglist_data.append(final)
        #             response = jsonify(shoppinglist_data)
        #             response.status_code = 200
        #             return response

        #     else:
        #         res = [shoppinglist for shoppinglist in
        #                response if shoppinglist.user_id == user_id]
        #         shoppinglist_data = []
                
        #         if not res:
        #             response = jsonify({
        #                  'error': 'No shoppinglists have been created'
        #             })
        #             response.status_code = 404
        #             return response
        #         else:
        #             for data in res:
        #                 final = {
        #                     'id': data.id,
        #                     'name': data.name,
        #                     'desc': data.desc,
        #                     'date_added': data.date_added,
        #                     'user_id': data.user_id,
                            
        #                 }
        #                 shoppinglist_data.append(final)
        #             response = jsonify(shoppinglist_data)
        #             response.status_code = 200
        #             return response






    @staticmethod
    def get_single_shoppinglist(user_id, shoppinglist_id):
        """
        Gets single shoppinglist
        :param user_id: 
        :param shoppinglist_id: 
        """
        shoppinglist = ShoppinglistModel.query.filter_by(id=shoppinglist_id,
                                             user_id=user_id).first()
        if not shoppinglist:
            response = jsonify({
                'error': 'shoppinglist with id ' +
                         str(shoppinglist_id) + ' not found'
            })
            response.status_code = 404
            return response

        shoppinglist_data = {
            'id': shoppinglist.id,
            'name': shoppinglist.name,
            'desc': shoppinglist.desc,
            'date_added': shoppinglist.date_added,
            'user_id': shoppinglist.user_id,
            
        }
        response = jsonify(shoppinglist_data)
        response.status_code = 200
        return response

    @staticmethod
    def update_shoppinglist(user_id, shoppinglist_id, shoppinglist_name, desc):
        """
        Updates a shoppinglist
                
        :param user_id: 
        :param shoppinglist_id: 
        :param shoppinglist_name: 
        :param desc:  
        """
        if not shoppinglist_name:
            response = jsonify({'Error': 'Missing shoppinglist name'})
            response.status_code = 400
            return response

        shoppinglist = ShoppinglistModel.query.filter_by(id=shoppinglist_id,
                                             user_id=user_id).first()
        if not shoppinglist:
            shoppinglist = jsonify({'error': 'the shoppinglist does not exist'})
            shoppinglist.status_code = 400
            return shoppinglist
        if shoppinglist.name is shoppinglist_name:
            shoppinglist = jsonify({'error': 'the shoppinglist name is the same'})
            shoppinglist.status_code = 409
            return shoppinglist
        shoppinglist.name = shoppinglist_name
        shoppinglist.desc = desc
        shoppinglist.update()

        shoppinglist = ShoppinglistModel.query.filter_by(id=shoppinglist_id,
                                             user_id=user_id).first()
        response = jsonify({'Success':'shoppinglist updated'
        })
        response.status_code = 200
        return response

    @staticmethod
    def delete_shoppinglist(user_id, shoppinglist_id):
        """
        Deletes a shoppinglist        
        :param user_id: 
        :param shoppinglist_id: 
        """
        shoppinglist = ShoppinglistModel.query.filter_by(id=shoppinglist_id,
                                             user_id=user_id).first()
        if not shoppinglist:
            response = jsonify({'error': 'shoppinglist not found'})
            response.status_code = 404
            return response

        items = ItemModel.query.filter_by(shoppinglist_id=shoppinglist_id)
        if items:
            for item in items:
                item.delete()

        shoppinglist.delete()
        response = jsonify({
            'success': 'shoppinglist deleted'
        })
        response.status_code = 200
        return response