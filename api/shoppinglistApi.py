import datetime

import jwt
from flask import redirect
from flask import jsonify, request, json, render_template
from api import create_app
from api.classes.authenticate import Authenticate
from api.classes.slists import ShoppingList
from api.classes.item import Item

app = create_app('ProductionEnv')

'''
 201  ok resulting to  creation of something
 200  ok
 400  bad request
 404  not found
 401  unauthorized
 409  conflict
'''

'''
    (UTF) Unicode Transformation Format
    its a character encoding
    A character in UTF8 can be from 1 to 4 bytes long
    UTF-8 is backwards compatible with ASCII
    is the preferred encoding for e-mail and web pages
'''


# 404 error handler
@app.errorhandler(404)
def page_not_found(e):
    response = jsonify({'error': 'The request can not be linked to, Please check your endpoint url'})
    response.status_code = 404
    return response


# 405 error handler
@app.errorhandler(405)
def method_not_allowed(e):
    response = jsonify({'error': 'Invalid request method. Please check the request method being used'})
    response.status_code = 405
    return response


# 401 error handler
@app.errorhandler(401)
def internal_server_error(e):
    response = jsonify({"error": "The token has a problem"})
    response.status_code = 401
    return response


# 500 error handler
@app.errorhandler(500)
def internal_server_error(e):
    response = jsonify({'error': 'something is wrong, please restart the server to use the shoppinglistAPI'})
    response.status_code = 500
    return response





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


def auth_success_reg(response):
    if response.status_code == 201:
        data = json.loads(response.data.decode())
        #data['token'] = encode_auth_token(data['token']).decode()
        response = jsonify(data)
        response.status_code = 201
    return response

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

        
        if isinstance(user_id, int):
            
            name = request.json['name']

            shop_name = name.lower()
            desc = request.json['desc']
            
            shoppinglist = ShoppingList()
            response = shoppinglist.create_shoppinglist(shop_name, desc, user_id)
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
            #Pagination arguments: Setting page to 1, then min_per_page to 20 and max_per_page to 100
            
            limit = request.args.get('limit',5,int)
            # if (type(limit) != int):
            #     response = jsonify({'Error': 'limit not an integer'})
            #     response.status_code = 404
            #     return response
            


            
            
            #limit = limit if limit <= 20 else 20
            search= request.args.get("q","")

            shoppinglist = ShoppingList()
            if limit:
                limit = int(limit)
                response = shoppinglist.get_shoppinglists(user_id,search,limit)
                return response
            response = shoppinglist.get_shoppinglists(user_id,search,limit)
            return response

        else:
            return invalid_token()

    except KeyError:
        return invalid_keys()


@app.route('/shoppinglists/', methods=['GET'])
def get_all_shoppinglists():
    """Method to handle getting all shoppinglists"""
    try:
        user_id = get_token()
        if isinstance(user_id, int):
            search = request.args.get("q", "")
            limit = request.args.get("limit", "")
            shoppinglist = ShoppingList()
            if limit:
                limit = int(limit)
                response = shoppinglist.get_all_shoppinglists(user_id, search, limit)
                return response
            response = shoppinglist.get_all_shoppinglists(user_id, search)
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
            shoppinglist_name = put_data['name']
            list_name = shoppinglist_name.lower()
            desc = put_data['desc']
            shoppinglist = ShoppingList()
            response = shoppinglist.update_shoppinglist(user_id, shoppinglist_id,
                                            list_name,desc)
            return response
        else:
            return invalid_token()

    except KeyError:
        return invalid_keys()


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


@app.route('/shoppinglists/<int:shoppinglist_id>/items', methods=['GET'])
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
            itemname = item_name.lower()
            item = Item()
            response = item.add_item(user_id, shoppinglist_id, itemname)
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
            new_item_name = request.json['item']
            newitemname = new_item_name.lower()
            #new_item_status = request.json['status']
            item = Item()
            response = item.edit_item(user_id, shoppinglist_id, item_id,
                                      newitemname)
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
    response = jsonify({'Error': 'There is a problem with token'})
    response.status_code = 401
    return response


def invalid_keys():
    response = jsonify({'Error': 'Check the keys and try again'})
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
    