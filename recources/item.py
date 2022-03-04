from flask import Flask,request
from flask_restful import Resource,Api,reqparse
from security import authenticate,identify
from models.user import *
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
import sqlite3
from models.item import ItemModel
from db import db
class Item(Resource):
    parser= reqparse.RequestParser()
    parser.add_argument('price',
        required=True,
        help="This field cannot be left blank",
        type=float
        )
    parser.add_argument('store_id',
        required=True,
        help="This field cannot be left blank",
        type=float
        )
    @jwt_required()
    def get(self,name):
        # item=next(filter(lambda x:x['name']== name, items),None)
        # return {'item':item},200 if item else 404

        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        else:
            return{"message":"item not found"},404
    
    

    def post(self,name):        

        if ItemModel.find_by_name(name):
            return {"message":"An item with name'{}' exist".format(name)}, 400
        data = Item.parser.parse_args()
        # item= {'name':name,
        # 'price': data['price']
        # }
        # items.append(item)
        item =ItemModel(name, data['price'],data['store_id'])
        try:
            item.save_to_db()
        except:
            return {"message":"Internal server error"},500

        return item.json(), 201
    
   

    def delete(self,name):
        # global items
        # items=list(filter(lambda x:x['name']!=name,items))

        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        
        # query = "DELETE FROM items WHERE name=?"
        # cursor.execute(query,(name,))
        # connection.commit()
        # connection.close()
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {"message":"Item deleted"}
    def put(self,name):
        
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        # updated_item= ItemModel(name,data['price'])
        if item is None:
            item = ItemModel(name, data['price'],data['store_id'])
        else:
            item.price= data['price']
        item.save_to_db()
        return item.json()
    
    
class ItemsList(Resource):
    @jwt_required()
    def get(self):
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        
        # query = "SELECT * FROM items"
        # result= cursor.execute(query)
        items=[]
        result= ItemModel.query.all()
        for row in result:
            
            items.append(row.json())
            
        # connection.commit()
        # connection.close()
        return {'items':items}