import json, jwt
import urllib.parse
import requests
from geopy.distance import geodesic
from flask import Blueprint, request, jsonify, current_app, Response
from flask_restful import Api, Resource # used for REST API building
from datetime import datetime
from auth_middleware import token_required

from model.users import User
from model.users import House

from model.users import House
house_api = Blueprint('house_api', __name__,
                   url_prefix='/api/house')
def createURL(address, k = "f81e24d4291f4b7a902958e6a02b7fe7"):
    encoded_address = urllib.parse.quote(address)

    url = f"https://api.geoapify.com/v1/geocode/search?text={encoded_address}&format=json&apiKey={k}"

    return url

api = Api(house_api)

class HouseAPI:     
    class _CRUD(Resource):
        def post(self):
            ''' Read data for json body '''
            body = request.get_json()
            price = body.get("price")
            beds = body.get("beds")
            baths = body.get("baths")
            address = body.get("address")
            lat = body.get("lat")
            long = body.get("long")
            sqfeet = body.get("sqfeet")
            ho = House (price, beds, baths, address, lat, long, sqfeet)
            ''' #2: Key Code block to add user to database '''
            # create player in database
            house = ho.create()
            # success returns json of player
            if house:
                return jsonify(house.read())
            # failure returns error
            return {'message': f'Error'}, 210

        def get(self):
            t = request.args.get('type')
            if t == "1":
                address = request.args.get('address')
                distance = int(request.args.get('distance'))
                json_ready = []
                url = createURL(address)
                response = requests.get(url)
                if response.status_code == 200:
                    response_json = response.json()
                    results = response_json.get('results')
                    if results and len(results) > 0:
                        first_result = results[0]
                        lon = first_result.get('lon')
                        lat = first_result.get('lat')
                        coord = (lat, lon)
                        house = House.query.all()
                        temp = [house.read() for house in house]
                        repeats = set() 
                        for h in temp:
                            hcoord = (h["lat"], h["long"])
                            dist = geodesic(coord, hcoord).miles
                            if dist <= distance and h["address"] not in repeats:
                                repeats.add(h["address"])
                                json_ready.append(h)
                return jsonify(json_ready)
            elif t == "2":
                address = request.args.get('address')
                for house in House.query.all():
                    if house.address == address:
                        return jsonify([house.read()])
                else:
                    return "err"
        
        def put(self):
            body = request.get_json() # get the body of the request
            price = body.get("price")
            beds = body.get("beds")
            baths = body.get("baths")
            address = body.get("address")
            sqfeet = body.get("sqfeet")
            house = House.query.get(address) # get the player (using the uid in this case)
            house.update(price = price, beds = beds, baths = baths, sqfeet = sqfeet)
            return f"{house.read()} Updated"

        def delete(self):
            token = request.cookies.get("jwt")
            if not token:
                return {
                    "message": "Authentication Token is missing!",
                    "data": None,
                    "error": "Unauthorized"
                }, 401
            try:
                data=jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
                if data["role"] == "Admin":
                    body = request.get_json()
                    print(body)
                    address = body.get('address')
                    houses = House.query.all()
                    count = 0
                    for house in houses:
                        print(house.address,address)
                        if house.address == address:
                            house.delete()
                            count+=1
                            if count == 2:
                                return f"{house.read()} Has been deleted"
                else: 
                    return {
                    "message": "Not an admin!",
                    "data": None,
                    "error": "Unauthorized"
                }, 401
            except Exception as e:
                return {
                    "message": "Something went wrong",
                    "data": None,
                    "error": str(e)
                }, 500


    # building RESTapi endpoint, method distinguishes action
    api.add_resource(_CRUD, '/')