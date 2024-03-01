from flask_app import app
from flask_app.controller import users 
from flask_app.controller import businesses 
from flask_app.controller import categories 
if __name__=="__main__":   
    app.run(debug=True, port = 5001)    