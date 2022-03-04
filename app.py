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
from db import db
app= Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATION']=False
api= Api(app)
app.secret_key= "jose"

@app.before_first_request
def create_table():
    db.create_all()


jwt= JWTManager(app)

class Login(Resource):
    def post(self):
        body=request.get_json()
        username= body['username']
        password= body['password']
        userid= authenticate(username, password)
        if userid != None:
            accesstoken= create_access_token(identity=str(userid))
            return {"accesstoken":accesstoken},200
        return {"message":"user not found"}
api.add_resource(Store,'/store/<string:name>')
api.add_resource(ItemsList,'/items')
api.add_resource(StoreList,'/stores')
api.add_resource(Item,'/items/<string:name>')
api.add_resource(Login,'/auth/login')
api.add_resource(UserRegister,'/register')


if __name__ == "__main__":
    from db import db
    db.init_app(app)
    app.run(port=5000,debug=True)