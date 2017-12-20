from flask import jsonify
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
            response.status_code = 404
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
    def get_shoppinglists(user_id, search, limit=None):
        """
        Gets all shoppinglists
        :param user_id: 
        :param search: 
        :return: 
        """
        response = ShoppinglistModel.query.filter_by(user_id=user_id).limit(limit).all()
        if not response:
            response = jsonify([])
            response.status_code = 200
            return response
        else:
            if search:
                res = [shoppinglist for shoppinglist in response if shoppinglist.name
                       in search and shoppinglist.user_id == user_id]
                if not res:
                    response = jsonify({
                        'error': 'The shoppinglist you searched does not exist'
                    })
                    return response
                else:
                    shoppinglist_data = []
                    for data in res:
                        final = {
                            'id': data.id,
                            'name': data.name,
                            'desc': data.desc,
                            'date_added': data.date_added,
                            'user_id': data.user_id
                            
                        }
                        shoppinglist_data.clear()
                        shoppinglist_data.append(final)
                    response = jsonify(shoppinglist_data)
                    response.status_code = 200
                    return response

            else:
                res = [shoppinglist for shoppinglist in
                       response if shoppinglist.user_id == user_id]
                shoppinglist_data = []
                
                if not res:
                    response = jsonify({
                         'error': 'No shoppinglists have been created'
                    })
                    response.status_code = 404
                    return response
                else:
                    for data in res:
                        final = {
                            'id': data.id,
                            'name': data.name,
                            'desc': data.desc,
                            'date_added': data.date_added,
                            'user_id': data.user_id,
                            
                        }
                        shoppinglist_data.append(final)
                    response = jsonify(shoppinglist_data)
                    response.status_code = 200
                    return response


# the query parameters
        # search_query = request.args.get('q', None, type=str)
        # page = request.args.get('page', 1, type=int)
        # per_page = request.args.get('limit', 10, type=int)
        # if per_page and per_page > 20:  # pragma: no cover
        #     per_page = 20
        # if not per_page or per_page < 1:  # pragma: no cover
        #     per_page = 20
        # if not page or page < 1:  # pragma: no cover
        #     page = 1

        # query_object = ShoppingList.query.filter(
        #     ShoppingList.user_id == user_id)
        # if search_query is not None:
        #     query_object = query_object.filter(ShoppingList.name.like(
        #         '%' + search_query.strip().lower() + '%'))

        # # pg_object refers to the pagination object obtained
        # pg_object = query_object.paginate(
        #     page=page, per_page=per_page, error_out=False)

        # next_page = None
        # if pg_object.has_next:
        #     next_page = "/api/v1/shoppinglists?page={0}{1}{2}".format(
        #         pg_object.next_num,
        #         '' if per_page == 20 else f'&limit={per_page}',
        #         '' if search_query is None else f'&q={search_query}')

        # previous_page = None
        # if pg_object.has_prev:
        #     previous_page = "/ shoppinglists?page={0}{1}{2}".format(
        #         pg_object.prev_num,
        #         '' if per_page == 20 else f'&limit={per_page}',
        #         '' if search_query is None else f'&q={search_query}')



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
            response.status_code = 200
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
            response.status_code = 200
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