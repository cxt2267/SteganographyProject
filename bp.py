from flask import Blueprint, render_template, redirect, url_for, request, jsonify, send_file, make_response
from DB import DB
import Steno
import io
import boto3

bp = Blueprint('bp',__name__)

db = DB()

@bp.route('/all-posts')
def all_posts():
    return jsonify(posts=db.allPosts())

@bp.route('/my-posts/<user>')
def my_posts(user):
    posts = db.userPosts(user)
    return jsonify(posts=posts)

@bp.route('/nav')
def nav():
    return render_template('nav.html')

@bp.route('/')
def home():    
    return render_template('index.html', posts=db.allPosts(), user=db.getUser(), logout="false", login="false")

@bp.route('/login', methods=["POST","GET"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        pswd = request.form["pswd"]
        usr = db.checkUser(email, pswd)
        if usr == "user not found":
            return render_template('login.html', error=usr)
        return render_template('index.html', user=db.getUser(), logout="false", login="true")
    return render_template('login.html')

@bp.route('/logout')
def logout():
    db.setUser("")
    return render_template('index.html', user=db.getUser(), logout="true", login="false")

@bp.route('/register', methods=["POST","GET"])
def register():
    if request.method == "POST":
        fname = request.form["fname"]
        lname = request.form["lname"]
        email = request.form["email"]
        pswd = request.form["pswd"]
        usr = db.regUser(fname, lname, email, pswd)
        if usr == "Email already in use.":
            return render_template('register.html', error=usr)
        elif usr == '''Password must contain at least 8 characters, an 
            uppercase letter, lowercase letter, a digit, and a special character.''':
            return render_template('register.html', error=usr)
        return render_template('index.html', user=db.getUser(), logout="false", login="true")
    return render_template('register.html')

@bp.route('/account')
def account():
    return render_template('account.html')

@bp.route('/upload/<user>', methods=["POST","GET"])
def upload(user):
    if request.method == "POST":
        post_info = {
            "carrier": request.files['carrier'],
            "message": request.files['message'],
            "start_bit": request.form['start_bit'],
            "period": request.form['period'],
            "op_mode": request.form['op_mode'],
            "post_name": request.form['post_name'],
            "user": int(user)
        }   
        result = Steno.createPost(post_info)
        if(result != "success"):
            return render_template('upload.html', error=result)
        return render_template('myposts.html')
    return render_template('upload.html')

@bp.route('/myposts')
def myposts():
    return render_template('myposts.html')

@bp.route('/fileblob', methods=['GET'])
def get_file_blob():
    file_path = request.args.get('file_path')

    s3_client = boto3.client('s3')
    s3_resp = s3_client.get_object(Bucket="stegaprojbucket", Key=file_path)

    file_content = s3_resp['Body'].read()
    file_blob = io.BytesIO(file_content)

    resp = make_response(send_file(file_blob, mimetype='application/octet-stream'))
    resp.headers["Content-Disposition"] = f"attachment; filename={file_path}"
    return resp