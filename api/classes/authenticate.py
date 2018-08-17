import re
from flask import jsonify
from validate_email import validate_email
from models.models import UserModel



class Authenticate(object):
    """
    Handles all user operations
    """

    @staticmethod
    def register(email, password, name):
        """
        Registers a new user to the application
        and returns an API response with status
        code set to 201 on success
        
        :param email: 
        :param password: 
        :param name:  
        """
        if not name or not email or not password:
            response = jsonify({'Error': 'Missing Values'})
            response.status_code = 404
            return response

        if type(name) is int:
            response = jsonify({'Error': 'Numbers cant be a Name'})
            response.status_code = 400
            return response

        if not re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email):
            response = jsonify(
            {'message':
            'Invalid email! A valid email should in this format me.name@gmail.com or joyce.namuli@andela.com' }
            )
            response.status_code = 401
            return response


        if re.match(r"(^[ ]*$)", name):
            response = jsonify(
            {'message':
            'A space is not a name' }
            )
            response.status_code = 401
            return response


        # if re.match(r"(^[ a-zA-Z_]*$)", name):
        #     response = jsonify(
        #     {'message':
        #     'Name dont start with spaces' }
        #     )
        #     response.status_code = 401
        #     return response

        if not re.match(r"(^[a-zA-Z_ ]*$)", name):
            response = jsonify(
            {'message':
            'Name should be in alphabetical' }
            )
            response.status_code = 401
            return response

        
        if len(password) < 6:
            response = jsonify({'Error': 'Password is short'})
            response.status_code = 400
            return response

        # if not name.isalpha():
        #     response = jsonify({'Error': 'Names must be in alphabetical strings'})
        #     response.status_code = 400
        #     return response

        user = UserModel(email=email, password=password, name=name)


        if user.query.filter_by(email=email).first():
            response = jsonify({'Error': 'Email Already exists'})
            response.status_code = 401
            return response

        user.save()
        response = jsonify({
            'Status': user.email + ' Successfully registered',
            'token': user.id
        })
        response.status_code = 201
        return response

    @staticmethod
    def login(email, password):
        """
        logs in an existing user to the application
        and returns an API response with status
        code set to 201 on success
        
        :param email: 
        :param password:  
        """
        if not email or not password:
            response = jsonify({'Error': 'Missing login credentials'})
            response.status_code = 400
            return response

        if not re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email):
            response = jsonify(
            {'message':
            'Invalid email! A valid email should in this format me.name@gmail.com or joyce.namuli@andela.com' }
            )
            response.status_code = 401
            return response

        user = UserModel(email=email, password=password)
        user_data = user.query.filter_by(email=email).first()

        # If Login successful
        if user_data and user.check_password(user_data.password,
                                             password):
            response = jsonify({
                'Status': user.email + ' Login Successful',
                'token': user_data.id
            })
            response.status_code = 201
            return response

        response = jsonify({'Error': 'Incorrect email or password'})
        response.status_code = 401
        return response




    

    @staticmethod
    def reset_password(email, old_password, new_password):
        """
        resets password of an existing user
        and returns an API response with status
        code set to 201 on success
        
        :param email: 
        :param old_password: 
        :param new_password: 
        :return: 
        """
        if not email or not old_password or not new_password:
            response = jsonify({'Error': 'Missing email or password'})
            response.status_code = 400
            return response

        user = UserModel.query.filter_by(email=email).first()

        # if user and user.check_password(user.password,
        #                                      old_password):

        if not user or not user.check_password(user.password, old_password):
            response = jsonify({'Error': 'Email and password does not exist'})
            response.status_code = 400
            return response

        user.password = new_password
        user.update()
        response = jsonify({
            'success': 'password updated',
        })
        response.status_code = 200
        return response
