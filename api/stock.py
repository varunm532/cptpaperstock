import json, jwt
from flask import Blueprint, request, jsonify, current_app, Response
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_restful import Api, Resource # used for REST API building
from datetime import datetime
from auth_middleware import token_required
from model.users import User, Stocks, Stock_Transactions
#from auth_middleware1 import token_required1
import sqlite3
from __init__ import app, db, cors, dbURI




from model.users import Stocks,User,Stock_Transactions

stocks_api = Blueprint('stocks_api', __name__,
                   url_prefix='/api/stocks')
api = Api(stocks_api)

class StocksAPI(Resource):
    class _Displaystock(Resource):
        #@token_required1("Admin")
        def get(self):
            stocks = Stocks.query.all()
            json_ready = [stock.read() for stock in stocks]
            return jsonify(json_ready)
    class _Transactionsdisplay(Resource):
        #@token_required1("Admin")
        
        def get(self):
            transaction = Stock_Transactions.query.all()
            json_ready = [transactions.read() for transactions in transaction]
            return jsonify(json_ready)
    #class _Transaction(Resource):
    #    def post(self):
    #        conn=sqlite3.connect('instance/volumes/sqlite.db')
    #        cur=conn.cursor()
    #        body = request.get_json()
    #        quantity = body.get('newquantity')
    #        symbol = body.get('symbol')
    #        update_query = "UPDATE stocks SET _quantity = ? WHERE _symbol = ?"
    #        #updatedstocks = Stocks.read() in symbol - symbols
    #        #Stocks.update(update_query, (quantity, symbol))
    #        cur.execute(update_query,(quantity,symbol))
    #        conn.commit()
    #        cur.close()
    class _Transaction1(Resource):
        def post(self):
            body = request.get_json()
            quantitytobuy = body.get('buyquantity')
            uid = body.get('uid')
            symbol = body.get('symbol')
            ##orginalquantity = body.get('avaliablequantity')
            newquantity = body.get('newquantity')
            transactiontype= 'buy'
            dob = body.get('dob')
            if dob is not None:
                try:
                    transactiondate = datetime.strptime(dob, '%Y-%m-%d').date()
                except:
                    return {'message': f'Date of birth format error {dob}, must be mm-dd-yyyy'}, 400
            ## update for stocks table to change the amound of stocks left
            stocks = Stocks.query.all()
            json_ready = [stock.read() for stock in stocks]
            list1 = [item for item in json_ready if item.get('symbol') == symbol]
            #users = User.query.all()
            #users = User.query.filter(User._uid == uid).all()
            #user_ids = [user.id for user in User.query.filter(User._uid == uid).first()]
            #user_ids = User.query.filter(User._uid == uid).first()
            user_ids = User.query.filter(User._uid == uid).value(User.id)
          
            print(user_ids)
            #json_ready_user1 = [user.read() for user in users]
            #list2 = [item for item in json_ready_user1 if item.get('uid') == uid]
            ##print(list2)
            #usermoney = list2[0]['stockmoney']
            #usermoney = [user.stockmoney for user in User.query.filter(User._uid == uid ).first()]
            #usermoney = User.query.filter(User._uid == uid ).first()
            usermoney = User.query.filter(User._uid == uid).value(User._stockmoney)
            
            print(usermoney)
            #currentstockmoney = list1[0]['sheesh']
            #currentstockmoney = [stocks.sheesh for stocks in Stocks.query.filter(Stocks._symbol == symbol ).first()]
            #currentstockmoney = Stocks.query.filter(Stocks._symbol == symbol ).first()
            currentstockmoney = Stocks.query.filter(Stocks._symbol == symbol).value(Stocks._sheesh)
            print(currentstockmoney)
            if (usermoney > currentstockmoney*quantitytobuy):
                ## updates stock quantity in stocks table
                tableid = list1[0]['quantity']
                print(tableid)
                tableid = list1[0]['id']
                tableid = Stocks.query.get(tableid)
                tableid.update(quantity=newquantity )
                db.session.commit()
                ## updates user money
                #tableid_user = list2[0]['id']
                updatedusermoney = usermoney - (currentstockmoney*quantitytobuy)
                print(updatedusermoney)
                #tableid_user = User.query.get(tableid_user)
                tableid_user = User.query.get(user_ids)
                print(tableid_user)
                #tableid_user.update(stockmoney=updatedusermoney)
                tableid_user.stockmoney = updatedusermoney
                #User.update(stockmoney=updatedusermoney)
                db.session.commit()
                ## creates log for transaction
                transactionamount = currentstockmoney*quantitytobuy
                #ta = Transactions(uid=uid, symbol=symbol,transaction_type=transactiontype, quantity=quantitytobuy, transaction_amount=transactionamount)
               # print(ta)
                #ta.create()   
                db.session.commit()
            else:
                return jsonify({'error': 'Insufficient funds'}), 400
                
            ##This is test.
            ##print("this is list1")
            ##print(str(list1[0]['quantity']))
            ##tableid = list1[0]['id']
            ##tableid = Stocks.query.get(tableid)
            ##tableid.update(quantity=newquantity )
            ##db.session.commit()
            ##
            ###chaning the total stock money
            ##users = User.query.all()
            ##json_ready_user = [user.read() for user in users]
            ##list2 = [item for item in json_ready_user if item.get('uid') == uid]
            ##tableid_user = list2[0]['id']
            ##tableid_user.update(stockmoney=newstockmoney)
            ##db.session.commit()
            ##
            ###creating transaction log
            ##ta = Transactions(uid=uid, symbol=symbol,transactiontype=transactiontype, quantity=oldquantity, transaction_amount=transactionamount, transaction_date=transactiondate )
            ##ta.create()   
            ##db.session.commit()
    class _Transaction2(Resource):
        ## updated 
        def post(self):
            body = request.get_json()
            quantitytobuy = body.get('buyquantity')
            uid = body.get('uid')
            symbol = body.get('symbol')
            ##orginalquantity = body.get('avaliablequantity')
            newquantity = body.get('newquantity')
            transactiontype= 'buy'
            ##attributes = {'transaction_date': current_timestamp}
            

# Print or use the variable as needed
            
            ## update for stocks table to change the amound of stocks left
            stocks = Stocks.query.all()
            json_ready = [stock.read() for stock in stocks]
            list1 = [item for item in json_ready if item.get('symbol') == symbol]
            #users = User.query.all()
            #users = User.query.filter(User._uid == uid).all()
            #user_ids = [user.id for user in User.query.filter(User._uid == uid).first()]
            #user_ids = User.query.filter(User._uid == uid).first()
            user_ids = User.query.filter(User._uid == uid).value(User.id)
          
            print(user_ids)
            #json_ready_user1 = [user.read() for user in users]
            #list2 = [item for item in json_ready_user1 if item.get('uid') == uid]
            ##print(list2)
            #usermoney = list2[0]['stockmoney']
            #usermoney = [user.stockmoney for user in User.query.filter(User._uid == uid ).first()]
            #usermoney = User.query.filter(User._uid == uid ).first()
            usermoney = User.query.filter(User._uid == uid).value(User._stockmoney)
            
            print(usermoney)
            #currentstockmoney = list1[0]['sheesh']
            #currentstockmoney = [stocks.sheesh for stocks in Stocks.query.filter(Stocks._symbol == symbol ).first()]
            #currentstockmoney = Stocks.query.filter(Stocks._symbol == symbol ).first()
            currentstockmoney = Stocks.query.filter(Stocks._symbol == symbol).value(Stocks._sheesh)
            print(currentstockmoney)
            if (usermoney > currentstockmoney*quantitytobuy):
                ## updates stock quantity in stocks table
                tableid = list1[0]['quantity']
                print(tableid)
                tableid = list1[0]['id']
                tableid = Stocks.query.get(tableid)
                tableid.update(quantity=newquantity )
                db.session.commit()
                ## updates user money
                #tableid_user = list2[0]['id']
                updatedusermoney = usermoney - (currentstockmoney*quantitytobuy)
                print(updatedusermoney)
                #tableid_user = User.query.get(tableid_user)
                tableid_user = User.query.get(user_ids)
                print(tableid_user)
                #tableid_user.update(stockmoney=updatedusermoney)
                tableid_user.stockmoney = updatedusermoney
                #User.update(stockmoney=updatedusermoney)
                db.session.commit()
                ## creates log for transaction
                transactionamount = currentstockmoney*quantitytobuy
                db.session.commit()
                Inst_table = Stock_Transactions(uid=uid, symbol=symbol,transaction_type=transactiontype, quantity=quantitytobuy, transaction_amount=transactionamount)
                print(Inst_table)
                Inst_table.create()   
                db.session.commit()
            else:
                return jsonify({'error': 'Insufficient funds'}), 400
                
            ##This is test.
            ##print("this is list1")
            ##print(str(list1[0]['quantity']))
            ##tableid = list1[0]['id']
            ##tableid = Stocks.query.get(tableid)
            ##tableid.update(quantity=newquantity )
            ##db.session.commit()
            ##
            ###chaning the total stock money
            ##users = User.query.all()
            ##json_ready_user = [user.read() for user in users]
            ##list2 = [item for item in json_ready_user if item.get('uid') == uid]
            ##tableid_user = list2[0]['id']
            ##tableid_user.update(stockmoney=newstockmoney)
            ##db.session.commit()
            ##
            ###creating transaction log
            #ta = Transactions(uid=uid, symbol=symbol,transaction_type=transactiontype, quantity=quantitytobuy, transaction_amount=transactionamount)
            #ta.create()   
            #db.session.commit()
    class _Transactionsdisplayuser(Resource):
        #@token_required1("Admin")
        def post(self):
            body =request.get_json()
            uid = body.get('uid')
            return uid
            
        def get(self):
            transaction = Stock_Transactions.query.all()
            json_ready = [transactions.read() for transactions in transaction]
            return jsonify(item for item in json_ready if item.get('uid') == post.uid)         
            

            
            
            
        
    api.add_resource(_Displaystock, '/stock/display')
    api.add_resource(_Transactionsdisplay, '/transaction/displayadmin')
    api.add_resource(_Transactionsdisplayuser, '/transaction/display')
    api.add_resource(_Transaction2, '/transaction')


            
        
    
        
        