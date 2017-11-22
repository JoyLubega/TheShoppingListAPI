import datetime

import jwt
from flask import jsonify, request, json, render_template
from api import create_app
from api.classes.authenticate import Authenticate
from api.classes.slists import ShoppingList
from api.classes.item import Item

app = create_app('ProductionEnv')


@app.route('/', methods=['GET'])
def index():
    """Index route"""
    return render_template('index.html')


@app.route('/auth/register', methods=['POST'])
def register():
    """Method to handle user registration"""
    request.get_json(force=True)
    try:
        name = request.json['name']
        email = request.json['email']
        password = request.json['password']
        user = Authenticate()
        response = user.register(email, password, name)
        response = auth_success(response)
        return response

    except KeyError:
        return invalid_keys()


@app.route('/auth/login', methods=['POST'])
def login():
    """Method to handle user login"""
    request.get_json(force=True)
    try:
        email = request.json['email']
        password = request.json['password']
        user = Authenticate()
        response = user.login(email, password)
        response = auth_success(response)
        return response

    except KeyError:
        return invalid_keys()


def auth_success(response):
    if response.status_code == 201:
        data = json.loads(response.data.decode())
        data['token'] = encode_auth_token(data['token']).decode()
        response = jsonify(data)
        response.status_code = 201
    return response


@app.route('/auth/reset-password', methods=['POST'])
def reset_password():
    """Method to handle reset password"""
    request.get_json(force=True)
    try:
        email = request.json['email']
        old_password = request.json['old_password']
        new_password = request.json['new_password']
        user = Authenticate()
        response = user.reset_password(email, old_password, new_password)
        return response

    except KeyError:
        return invalid_keys()


@app.route('/shoppinglists', methods=['POST'])
def add_shoppinglist():
    """Method to handle creating a shoppinglist"""
    request.get_json(force=True)
    try:
        user_id = get_token()
        #print(user_id.data)
        if isinstance(user_id, int):
            name = request.json['shoppinglist']
            desc = request.json['desc']
            shoppinglist = ShoppingList()
            response = shoppinglist.create_shoppinglist(name, desc, user_id)
            return response
            
        return invalid_token()

    except KeyError:
        return invalid_keys()


@app.route('/shoppinglists', methods=['GET'])
def get_shoppinglists():
    """Method to handle getting all shoppinglists"""
    try:
        user_id = get_token()
        if isinstance(user_id, int):
            search = request.args.get("q", "")
            limit = request.args.get("limit", "")
            shoppinglist = ShoppingList()
            if limit:
                limit = int(limit)
                response = shoppinglist.get_shoppinglists(user_id, search, limit)
                return response
            response = shoppinglist.get_shoppinglists(user_id, search)
            return response

        else:
            return invalid_token()

    except KeyError:
        return invalid_keys()


@app.route('/shoppinglists/<int:shoppinglist_id>', methods=['GET'])
def get_single_shoppinglist(shoppinglist_id):
    """Method to handle getting a single list"""
    try:
        user_id = get_token()
        if isinstance(user_id, int):
            shoppinglist = ShoppingList()
            response = shoppinglist.get_single_shoppinglist(user_id, shoppinglist_id)
            return response
        else:
            return invalid_token()

    except KeyError:
        return invalid_keys()


@app.route('/shoppinglists/<int:shoppinglist_id>', methods=['PUT'])
def update_shoppinglist(shoppinglist_id):
    """Method to handle updating a shoppinglist"""
    # (request)
    put_data = request.get_json(force=True)
    # (request.data)
    try:
        user_id = get_token()
        if isinstance(user_id, int):
            shoppinglist_name = put_data['shoppinglist']
            desc = put_data['desc']
            shoppinglist = ShoppingList()
            response = shoppinglist.update_shoppinglist(user_id, shoppinglist_id,
                                            shoppinglist_name, desc)
            return response
        else:
            return invalid_token()

    except KeyError:
        return invalid_keys()




# @app.route('/shoppinglists/<int:shoppinglist_id>', methods=['PUT'])
# def update_shoppinglist(shoppinglist_id):
#     """Method to handle updating a shoppinglist"""
#     request.get_json(force=True)
    
#     try:
#         print("joy")
#         shoppinglist_id= request.json['shoppinglist_id']
#         old_name = request.json['old_name']
#         new_name = request.json['new_name']
        
#         if  not old_name:
#             return 404
#         elif old_name is new_name:
#             return 400
#         else:
#             return response
#         shoppinglist = ShoppingList()
#         response = shoppinglist.update_shoppinglist(user_id,ushoppinglist_id, old_name, new_name)
#     except KeyError:
#         return invalid_keys()


@app.route('/shoppinglists/<int:shoppinglist_id>', methods=['DELETE'])
def delete_shoppinglist(shoppinglist_id):
    """Method to handle creating a shoppinglist"""
    try:
        user_id = get_token()
        if isinstance(user_id, int):
            shoppinglist = ShoppingList()
            response = shoppinglist.delete_shoppinglist(user_id, shoppinglist_id)
            return response
        else:
            return invalid_token()

    except KeyError:
        return invalid_keys()


@app.route('/items/<int:shoppinglist_id>', methods=['GET'])
def get_items(shoppinglist_id):
    """Method to handle getting all items in a shoppinglist"""
    try:
        user_id = get_token()
        if isinstance(user_id, int):
            item = Item()
            response = item.get_items(shoppinglist_id)
            return response
        else:
            return invalid_token()

    except KeyError:
        return invalid_keys()


@app.route('/shoppinglists/<int:shoppinglist_id>/items', methods=['POST'])
def add_item(shoppinglist_id):
    """Method to handle creating a shoppinglist"""
    request.get_json(force=True)
    try:
        user_id = get_token()
        if isinstance(user_id, int):
            item_name = request.json['item']
            item = Item()
            response = item.add_item(user_id, shoppinglist_id, item_name)
            return response
        else:
            return invalid_token()

    except KeyError:
        return invalid_keys()


@app.route('/shoppinglists/<int:shoppinglist_id>/items/<int:item_id>', methods=['PUT'])
def edit_item(shoppinglist_id, item_id):
    """Method to handle creating a shoppinglist"""
    request.get_json(force=True)
    try:
        user_id = get_token()
        if isinstance(user_id, int):
            item_name = request.json['item']
            item_status = request.json['status']
            item = Item()
            response = item.edit_item(user_id,shoppinglist_id , item_id,
                                      item_name, item_status)
            return response
        else:
            return invalid_token()

    except KeyError:
        return invalid_keys()


@app.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    """Method to handle creating a shoppinglist"""
    try:
        token = get_token()
        if isinstance(token, int):
            item = Item()
            response = item.delete_item(item_id)
            return response
        else:
            return invalid_token()

    except KeyError:
        return invalid_keys()


def invalid_token():
    response = jsonify({'Error': 'Invalid Token'})
    response.status_code = 401
    return response


def invalid_keys():
    response = jsonify({'Error': 'Invalid Keys detected'})
    response.status_code = 401
    return response


def get_token():
    return decode_auth_token(request.headers.get("Authorization"))


def encode_auth_token(user_id):
    """
    Generates the Auth Token
    :return: string
    """
    try:
        payload = {
            'exp': datetime.datetime.utcnow() +
                   datetime.timedelta(days=90),
            'iat': datetime.datetime.utcnow(),
            'sub': user_id
        }
        return jwt.encode(
            payload,
            app.config.get('SECRET_KEY'),
            algorithm='HS256'
        )
    except Exception as e:
        return e


def decode_auth_token(token):
    """
    Decodes the auth token
    :param auth_token:
    :return: integer|string
    """
    try:
        payload = jwt.decode(token, app.config.get('SECRET_KEY'), algorithms=['HS256'])
        return payload['sub']
    except jwt.ExpiredSignatureError:
        response = jsonify({
            'Expired': 'Signature expired. Please log in again.'
        })
        response.status_code = 401
        return response

    except jwt.InvalidTokenError:
        response = jsonify({
            'Invalid': 'Invalid token. Please log in again.'
        })
        response.status_code = 401
        return response
        
       