import sqlite3
from flask_restful import Resource,reqparse
from models.user import UserModel
from blocklist import BLOCKLIST
from flask_jwt_extended import create_access_token,create_refresh_token,jwt_required,get_jwt_identity,get_jwt

class UserRegister(Resource):
    parser= reqparse.RequestParser()
    parser.add_argument('username',
            type=str,
            required=True,
            help="This field cannot be empty"
        )
    parser.add_argument('password',
            type=str,
            required=True,
            help="This field cannot be empty"
        )
    def post(self):
        data =UserRegister.parser.parse_args()
        
        if UserModel.find_by_username(data['username']) != None:
            return {"message":"User already Exists"}
        # connection = sqlite3.connect('data.db')
        # cursor= connection.cursor()

        # query="INSERT INTO users VALUES (NULL,?,?)"
        # cursor.execute(query,(data['username'], data['password']))

        # connection.commit()
        # connection.close()
        user = UserModel(data['username'], data['password'])
        user.save_to_db()
        return {"message":"Users Created Successfully"},201

class User(Resource):
    @classmethod    
    def get(cls,user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message':'user not found'},404
        return user.json()

    

    @classmethod
    def delete(cls,user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message':'user not found'},404
        user.delete_from_db()
        return {'message': 'user deleted'},200

class UserLogin(Resource):
    parser= reqparse.RequestParser()
    parser.add_argument('username',
            type=str,
            required=True,
            help="This field cannot be empty"
        )
    parser.add_argument('password',
            type=str,
            required=True,
            help="This field cannot be empty"
        )


    @classmethod
    def post(cls):
        data = cls.parser.parse_args()
        
        user = UserModel.find_by_username(data['username'])

        if user and user.password==data['password']:
            access_token = create_access_token(identity=user.id,fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {
                'access_token':access_token,
                'refresh_token':refresh_token
            },200
        
        return {'message':'Invalid credentials'},401

class UserLogout(Resource):
    @jwt_required()
    def post(self):
        BLOCKLIST.add(get_jwt()['jti'])
        return {'message':'Succesfully logout'}
class TokenRefresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user, fresh=False)
        return {'access_token':access_token}