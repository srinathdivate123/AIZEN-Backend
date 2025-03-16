from flask_restx import Resource, Namespace, fields
from models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
    create_access_token,
    get_jwt_identity,
    jwt_required,
)
from flask import request, jsonify, make_response


auth_ns = Namespace("auth", description="A namespace for our Authentication")


register_model = auth_ns.model(
    "Register",
    {
        "name": fields.String(required=True),
        "email": fields.String(required=True),
        "password": fields.String(required=True),
    },
)

login_model = auth_ns.model(
    "Login", 
    {
        "email": fields.String(required=True),
        "password": fields.String(required=True)
    }
)


@auth_ns.route("/register")
class Register(Resource):
    @auth_ns.expect(register_model, validate=True)
    def post(self):
        data = request.get_json()
        email = data.get("email")
        db_user = User.query.filter_by(email=email).first()
        
        if db_user is not None:
            return jsonify({"message": f"User with email {email} already exists. Please choose another email."})

        new_user = User(
            username=data.get("name"),
            email=email,
            password=generate_password_hash(data.get("password")),
        )

        new_user.save()
        return make_response(jsonify({"message": "User created successfuly!"}), 201)


@auth_ns.route("/login")
class Login(Resource):
    @auth_ns.expect(login_model, validate=True)
    def post(self):
        data = request.get_json()

        email = data.get("email")
        password = data.get("password")

        db_user = User.query.filter_by(email=email).first()

        if db_user and check_password_hash(db_user.password, password):

            access_token = create_access_token(identity=db_user.email)

            return jsonify(
                {"access_token": access_token, "user": db_user.to_dict()}
            )

        else:
            return make_response(jsonify({"message": "Sorry! Your credentials don't match!"}), 404)



@auth_ns.route('/current-user')
class CurrentUser(Resource):
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        db_user = User.query.filter_by(email=current_user).first()
        if not db_user:
            return jsonify({"error":" User not found!"}), 404
        return jsonify({"user": db_user.to_dict()})