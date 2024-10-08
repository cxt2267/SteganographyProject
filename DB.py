import mysql.connector
import bcrypt
import json
import os
import re
import boto3
from botocore.exceptions import ClientError

class DB:
    user_info = ""  

    def getUser(self):
        return self.user_info
    
    def setUser(self, info):
        user_info = info

    def getDBSecret(self):
        secret_name = "StegaProj-DBCred"
        region_name = "us-east-1"

        session = boto3.session.Session()
        client = session.client(
            service_name='secretsmanager',
            region_name=region_name
        )

        try:
            secret_value_resp = client.get_secret_value(
                SecretId=secret_name
            )
            return json.loads(secret_value_resp['SecretString'])
        except ClientError as e:
            raise e

    def conn(self):
        dbSecret = self.getDBSecret()
        con = mysql.connector.connect(
            host = dbSecret['host'],
            user = dbSecret['username'],
            password = dbSecret['password'],
            database = dbSecret['dbName']
        )
        if con.is_connected():
            return con

    def hash(self, pswd):
        return bcrypt.hashpw(pswd.encode('utf-8'),bcrypt.gensalt())

    def checkPass(self, pswd):
        if len(pswd) < 8:
            return False
        elif not bool(re.search(r'[A-Z]', pswd)):
            return False
        elif not bool(re.search(r'[a-z]', pswd)):
            return False
        elif not bool(re.search(r'[0-9]', pswd)):
            return False
        elif not bool(re.search(r'[^a-zA-Z0-9]', pswd)):
            return False
        return True

    def regUser(self, fname, lname, email, pswd):
        if self.emailExists(email) :
            return "Email already in use."
        if not self.checkPass(pswd) :
            return '''Password must contain at least 8 characters, an 
            uppercase letter, lowercase letter, a digit, and a special character.'''
            
        con = self.conn()
        curs = con.cursor()
        stmt = "insert into Users(Fname, Lname, Email, Pswd) values(%s, %s, %s, %s)"
        values = (fname.strip(), lname.strip(), email.strip(), self.hash(pswd))
        curs.execute(stmt, values)
        con.commit()
        stmt = "select * from Users where Email = %s"
        values = [email.strip()]
        curs.execute(stmt, values)
        user = curs.fetchall()
        con.close()
        s3_client = boto3.client('s3')
        s3_client.put_object(Bucket="stegaprojbucket", Key=(f"user_{user[0][0]}/"))

        user = self.checkUser(email, pswd)
        self.user_info = user
        return self.user_info

    def emailExists(self, email):
        con = self.conn()
        curs = con.cursor()
        stmt = "select * from Users where Email = %s"
        values = [email.strip()]
        curs.execute(stmt, values)
        user = curs.fetchall()
        con.close()
        if user :
            return True
        else :
            return False

    def checkUser(self, email, pswd):
        con = self.conn()
        curs = con.cursor()
        stmt = "select * from Users where Email = %s"
        values = [email.strip()]
        curs.execute(stmt, values)
        user = curs.fetchall()
        con.close()
        if user :
            pswdhash = user[0][4]
            if not bcrypt.checkpw(pswd.encode('utf-8'), pswdhash.encode('utf-8')):
                return "user not found"
        else :
            return "user not found"
        
        user_tuple = {
            "UserID": f"{user[0][0]}",
            "Fname": f"{user[0][1]}",
            "Lname": f"{user[0][2]}",
            "Email": f"{user[0][3]}",
            "Password": f"{pswd}"
        }

        self.user_info = json.dumps(user_tuple)
        return self.user_info
    
    def addPost(self, post_info):
        post = post_info["post"]
        carr = post_info["carrier"].filename
        msg = post_info["message"].filename
        stbit = post_info["stbit"]
        per = post_info["per"]
        user = post_info["user"]

        con = self.conn()
        curs = con.cursor()
        stmt = "insert into Posts(Post, Carrier, Message, StartBit, Period, UserID) values(%s, %s, %s, %s, %s, %s)"
        values = (post, carr, msg, stbit, per, user)
        curs.execute(stmt, values)
        con.commit()
        con.close()

    def userPosts(self, user):
        con = self.conn()
        curs = con.cursor()
        stmt = "select * from Posts where UserID = %s"
        values = [user]
        curs.execute(stmt, values)
        posts = curs.fetchall()
        post_paths = []
        for post in posts:
            ext_ind = post[2].rfind('.')
            ext = post[2][ext_ind:]
            post_paths.append(f"user_{post[6]}/{post[1]}/{post[1]}{ext}") 
        con.close()
        return post_paths

    def allPosts(self):
        con = self.conn()
        curs = con.cursor()
        stmt = "select * from Posts"
        curs.execute(stmt)
        posts = curs.fetchall()
        post_paths = []
        for post in posts:
            ext_ind = post[2].rfind('.')
            ext = post[2][ext_ind:]
            post_paths.append(f"user_{post[6]}/{post[1]}/{post[1]}{ext}")
        con.close()
        return post_paths
    
    def getPost(self, post_name):
        con = self.conn()
        curs = con.cursor()
        stmt = "select * from Posts where Post = %s"
        values = [post_name]
        curs.execute(stmt, values)
        post = curs.fetchall()
        con.close()
        if not post:
            return None
        else:
            return post[0]
        