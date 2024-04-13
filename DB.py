import mysql.connector
import bcrypt
import json
import File

class DB:
    user_info = ""  

    def getUser(self):
        return self.user_info
    
    def setUser(self, info):
        user_info = info

    def conn(self):
        con = mysql.connector.connect(
            host = "stega-proj.cfs6c6cwccjc.us-east-1.rds.amazonaws.com",
            user = "admin",
            password = "cse4381Stega",
            database = "StegaProj"
        )
        if con.is_connected():
            return con

    def hash(self, pswd):
        return bcrypt.hashpw(pswd.encode('utf-8'),bcrypt.gensalt())

    def regUser(self, fname, lname, email, pswd):
        if self.emailExists(email) :
            return "email already in use"
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
        File.createUserFold(user[0][0])
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
        post = post_info["post"].name
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
        postnames = []
        for post in posts:
            #ext_ind = post[2].rfind('.')
            #ext = post[2][ext_ind:]
            #postfile = post[1] + ext
            postnames.append(post[1])
        con.close()
        return postnames

    def allPosts(self):
        con = self.conn()
        curs = con.cursor()
        stmt = "select * from Posts"
        curs.execute(stmt)
        posts = curs.fetchall()
        postfiles = []
        for post in posts:
            ext_ind = post[2].rfind('.')
            ext = post[2][ext_ind:]
            postfile = post[1] + ext
        con.close()
    
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
        


