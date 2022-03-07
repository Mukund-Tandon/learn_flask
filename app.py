import os
from flask import Flask,request
from flask_restful import Resource,Api,reqparse
from security import authenticate,identify
from recources.user import *
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from recources.item import Item,ItemsList
from recources.store import Store ,StoreList
from blocklist import BLOCKLIST
from db import db
app= Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']=os.environ.get('DATABASE_URL','sqlite:///data.db')#second one is the default value
app.config['SQLALCHEMY_TRACK_MODIFICATION']=False
app.config['PROPOGATE_EXCEPTIONS']=True 
app.config['JWT_BLACKLIST_ENABLED']=True
app.config['JWT_BLACKLIST_TOKEN_CHECKS']=['access','refresh']
api= Api(app)
app.secret_key= "jose"

@app.before_first_request
def create_table():
    db.create_all()


jwt= JWTManager(app)
@jwt.additional_claims_loader
def add_claims_to_jwt(identity):
    if identity ==1:
        return {'is_admin': True}
    return {'is_admin':False} 
    
@jwt.expired_token_loader
def expired_token_callback(jwt_header,jwt_payload):
    return {
        'description':'The token has expired ',
        'error': 'token_expired'
    },401

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return {
        'description':'Signature verification failed',
        'error':'token_expired'
    },401

@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({
        'description':'The token is not fresh',
        'error':'fresh_token_required'
    }),401

@jwt.revoked_token_loader
def revoked_token_callback(jwt_header,jwt_payload):
    return {
        'description':'The token has been revoked',
        'error': 'fresh_token_required'
    },401

@jwt.token_in_blocklist_loader#userlogout
def check_if_token_in_blacklist(jwt_header,jwt_payload):
    print(jwt_payload)
    return jwt_payload['jti'] in BLOCKLIST
api.add_resource(Store,'/store/<string:name>')
api.add_resource(ItemsList,'/items')
api.add_resource(StoreList,'/stores')
api.add_resource(Item,'/items/<string:name>')
api.add_resource(UserLogin,'/auth/login')
api.add_resource(UserRegister,'/register')
api.add_resource(User,'/user/<int:user_id>')
api.add_resource(TokenRefresh, '/refresh')
api.add_resource(UserLogout, '/logout')
if __name__ == "__main__":
    from db import db
    db.init_app(app)
    app.run(port=5000,debug=True)