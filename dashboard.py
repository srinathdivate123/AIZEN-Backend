from flask_restx import Namespace, Resource
from models import ImageData, User
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request, current_app
from models import db, ImageData
from flask import request, jsonify
from werkzeug.utils import secure_filename
import datetime
import boto3
import uuid


 
ALLOWED_EXTENSIONS = set([ 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

workspace_ns = Namespace("dashboard", description="A namespace for dashboard")




@workspace_ns.route('/images')
class HandleImages(Resource):

    @jwt_required()
    def get(self):
        current_user_email = get_jwt_identity()
        db_user = User.query.filter_by(email=current_user_email).first()
        all_images = ImageData.query.filter_by(user_id = db_user.id)


        paths = []
        for img in all_images:
            p = 'https://' + 'aizenproject' + '.s3.us-east-1.amazonaws.com/' + img.filename
            paths.append(p)

        
        return jsonify({"paths": paths})

    @jwt_required()
    def post(self):
        current_user_email = get_jwt_identity()
        db_user = User.query.filter_by(email=current_user_email).first()

        user_id = db_user.id


        if 'files[]' not in request.files:
            resp = jsonify({
                "message": 'No file part in the request',
                "status": 'failed'
            })
            resp.status_code = 400
            return resp
    
        files = request.files.getlist('files[]')
        
        errors = {}
        success = False
        for file in files:      
            if file and allowed_file(file.filename):

                new_filename = uuid.uuid4().hex + '.' + file.filename.rsplit('.', 1)[1].lower()

                bucket_name = "aizenproject"
                s3 = boto3.resource("s3", aws_access_key_id = current_app.config['AWS_ACCESS_KEY'], aws_secret_access_key=current_app.config['AWS_SECRET_KEY'])
                s3.Bucket(bucket_name).upload_fileobj(file, new_filename)


    
                newFile = ImageData(original_filename = file.filename, filename=new_filename, upload_date = datetime.datetime.now(datetime.timezone.utc), user_id = user_id)
                
                db.session.add(newFile)
                db.session.commit()
    
                success = True
            else:
                resp = jsonify({
                    "message": 'File type is not allowed',
                    "status": 'failed'
                })
                return resp
        if success and errors:
            errors['message'] = 'File(s) successfully uploaded'
            errors['status'] = 'failed'
            resp = jsonify(errors)
            resp.status_code = 500
            return resp
        if success:
            resp = jsonify({
                "message": 'Files successfully uploaded',
                "status": 'success'
            })
            resp.status_code = 201
            return resp
        else:
            resp = jsonify(errors)
            resp.status_code = 500
            return resp


@workspace_ns.route("/workspace")
class Workspace(Resource):
    @jwt_required()
    def get(self):
        pass
