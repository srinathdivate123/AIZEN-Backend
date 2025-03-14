from flask_restx import Resource, Namespace, fields
from models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    jwt_required,
)
from flask import Flask, request, jsonify, make_response


auth_ns = Namespace("auth", description="A namespace for our Authentication")


signup_model = auth_ns.model(
    "SignUp",
    {
        "name": fields.String(),
        "email": fields.String(),
        "password": fields.String(),
    },
)


login_model = auth_ns.model(
    "Login", {"name": fields.String(), "password": fields.String()}
)


@auth_ns.route("/register")
class SignUp(Resource):
    @auth_ns.expect(signup_model)
    def post(self):
        data = request.get_json()
        name = data.get("name")
        db_user = User.query.filter_by(username=name).first()
        if db_user is not None:
            return jsonify({"message": f"User with name {name} already exists"})

        new_user = User(
            username=data.get("name"),
            email=data.get("email"),
            password=generate_password_hash(data.get("password")),
        )

        new_user.save()
        return make_response(jsonify({"message": "User created successfuly"}), 201)


@auth_ns.route("/login")
class Login(Resource):
    @auth_ns.expect(login_model)
    def post(self):
        data = request.get_json()

        email = data.get("email")
        password = data.get("password")

        db_user = User.query.filter_by(email=email).first()

        if db_user and check_password_hash(db_user.password, password):

            access_token = create_access_token(identity=db_user.email)
            refresh_token = create_refresh_token(identity=db_user.email)

            return jsonify(
                {"access_token": access_token, "refresh_token": refresh_token, "user": db_user.to_dict()}
            )

        else:
            return make_response(jsonify({"message": "Invalid name or password"}), 404)


@auth_ns.route("/refresh")
class RefreshResource(Resource):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_access_token = create_access_token(identity=current_user)
        return make_response(jsonify({"access_token": new_access_token}), 200)
    

@auth_ns.route('/user/current')
class CurrentUser(Resource):
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        db_user = User.query.filter_by(email=current_user).first()
        if not db_user:
            return jsonify({"error":" User not found!"})
        return jsonify({"user": db_user.to_dict()})