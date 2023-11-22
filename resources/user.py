import os 
import requests
from sqlite3 import IntegrityError
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    jwt_required,
    get_jwt,
)

from sqlalchemy import or_

from db import db
from blocklist import BLOCKLIST
from models import UserModel
from schemas import UserSchema, UserRegisterSchema


blp = Blueprint("Users", "users", description="Operations on users")

def send_simple_message(to, subject, body):
    domain = os.environ.get("MAILGUN_DOMAIN")
    print(os.getenv("MAILGUN_DOMAIN"))
    print(os.getenv("MAILGUN_API_KEY"))
    print(f"domain: {domain} - to: {to} - subject: {subject} - body: {body}")
    try:
        return requests.post(
            f"https://api.mailgun.net/v3/{domain}/messages",
            auth=("api", os.getenv("MAILGUN_API_KEY")),
            data={
                "from": f"Alan <mailgun@{domain}>",
                "to": [to],
                "subject": subject,
                "text": body
            }        
        )
    except Exception as e:
        print(f"An error occurred: {e}")
        return {"message": "An error occurred while sending the email"}, 500

@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(UserRegisterSchema)
    def post(self, user_data):
        if UserModel.query.filter(
            or_(
                UserModel.username == user_data["username"],
                UserModel.email == user_data["email"],
            )
        ).first():
            abort(409, message="A user with that username or email already exists.")
            
        user = UserModel(   
            username=user_data["username"],
            email=user_data["email"],
            password=pbkdf2_sha256.hash(user_data["password"])
        )
        db.session.add(user)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            abort(409, message="User already exists")
        
        send_simple_message(
            to=user.email,
            subject="Successfully signed up",
            body=f"Hi {user.username}! You have successfully signed up to the Stores REST API.",
        )
        
        return {"message": "User created successfully"}, 201

@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(UserSchema(only=("username", "password")))    
    def post(self, user_data):
        user = UserModel.query.filter_by(username=user_data["username"]).first()
        
        if user and pbkdf2_sha256.verify(user_data["password"], user.password):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(identity=user.id)
            return {"access_token": access_token, "refresh_token": refresh_token}, 200
        
        abort(401, message="Invalid credentials")

@blp.route("/refresh")
class TokenRefresh(MethodView):
    @jwt_required(refresh=True) # refresh token required not access token
    def post(self):
        current_user = get_jwt_identity() # same of get_jwt().get("sub")
        new_token = create_access_token(identity=current_user, fresh=False)
        # Make it clear that when to add the refresh token to the blocklist will depend on the app design        
        # In this way generate just one non fresh access_token for each fresh access_token in the input
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return {"access_token": new_token}, 200 

@blp.route("/logout")
class UserLogout(MethodView):
    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return {"message": "User logged out successfully"}, 200

@blp.route("/user/<int:user_id>")
class User(MethodView):
    """
    This resource can be useful when testing our Flask app.
    We may not want to expose it to public users, but for the
    sake of demonstration in this course, it can be useful
    when we are manipulating data regarding the users.
    """

    @blp.response(200, UserSchema)
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        return user

    def delete(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {"message": "User deleted."}, 200
