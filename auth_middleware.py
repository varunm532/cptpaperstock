from functools import wraps
import jwt
from flask import request, abort
from flask import current_app
from model.users import User

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        print(request.cookies)
        token = request.cookies.get("jwt")
        if not token:
            return {
                "message": "Authentication Token is missing!",
                "data": None,
                "error": "Unauthorized"
            }, 401
        try:
            data=jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
            print(data)
            current_user=User.query.filter_by(_uid=data["_uid"]).first()
            print(current_user)
            users = User.query.all()
            for user in users: 
                print(user.uid, data["_uid"])
                if user.uid == data["_uid"]:
                    current_user = user
                    break
            else: 
                print("here")
                return {
                "message": "Invalid Authentication token!",
                "data": None,
                "error": "Unauthorized"
            }, 401

            #if roles and current_user.role not in roles:
             #       return {
              #          "message": "Insufficient permissions. Required roles: {}".format(roles),
               #         "data": None,
                #        "error": "Forbidden"
                 #   }, 403
            
        except Exception as e:
            return {
                "message": "Something went wrong",
                "data": None,
                "error": str(e)
            }, 500

        return f(*args, **kwargs)

    return decorated