from flask import Flask
from bp import bp
import DB

app = Flask(__name__, static_folder='./static')
app.register_blueprint(bp)

if __name__ == '__main__':  
   app.run()