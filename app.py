from flask import Flask
from bp import bp
import DB
from flask_cors import CORS

app = Flask(__name__, static_folder='./static')
app.register_blueprint(bp)

CORS(app)

if __name__ == '__main__':  
   app.run()