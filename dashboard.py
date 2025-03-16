from flask_restx import Namespace, Resource
from models import ImageData, User
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request, current_app
from models import db, ImageData
from flask import request, jsonify
import datetime
import boto3
import uuid

 
ALLOWED_EXTENSIONS = set([ 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

dashboard_ns = Namespace("dashboard", description="A namespace for dashboard")


@dashboard_ns.route('/images')
class HandleImages(Resource):

    @jwt_required()
    def get(self):
        current_user_email = get_jwt_identity()
        db_user = User.query.filter_by(email=current_user_email).first()

        if not db_user:
            return jsonify({"error":" User not found!"}), 404
        
        all_images = ImageData.query.filter_by(user_id = db_user.id)


        paths = []
        for img in all_images:
            p = 'https://' + current_app.config['BUCKET_NAME'] + '.s3.us-east-1.amazonaws.com/' + img.filename
            paths.append(p)

        
        return jsonify({"paths": paths})

    @jwt_required()
    def post(self):
        current_user_email = get_jwt_identity()

        db_user = User.query.filter_by(email=current_user_email).first()
        if not db_user:
            return jsonify({"error":" User not found!"}), 404

        user_id = db_user.id

        file = request.files.get("files[]")

        if not allowed_file(file.filename):
            return jsonify({
                "message": "Invalid file format",
                "status": "failed"
            }), 400
    

        new_filename = uuid.uuid4().hex + '.' + file.filename.rsplit('.', 1)[1].lower()

        try:

            s3 = boto3.resource("s3", aws_access_key_id = current_app.config['AWS_ACCESS_KEY'], aws_secret_access_key=current_app.config['AWS_SECRET_KEY'])

            s3.Bucket(current_app.config['BUCKET_NAME']).upload_fileobj(file, new_filename)

            newFile = ImageData(original_filename = file.filename, filename=new_filename, upload_date = datetime.datetime.now(datetime.timezone.utc), user_id = user_id)
                    
            db.session.add(newFile)
            db.session.commit()

        except Exception as e:
            resp = jsonify({
                "message": 'Oops! There was an error in uploading your file',
                "status": 'failed'
            })
            resp.status_code = 400
            return resp


        resp = jsonify({
                "message": 'Files successfully uploaded',
                "status": 'success'
            })
        resp.status_code = 201
        return resp



@dashboard_ns.route("/analyse-ai")
class AnalyseAI(Resource):
    @jwt_required()
    def post(self):
        data = request.get_json()
        filename = data["filename"]
        print(filename)



@dashboard_ns.route("/")
class Workspace(Resource):
    @jwt_required()
    def get(self):
        pass