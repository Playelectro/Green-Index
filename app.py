from flask import Flask
from flask_restx import Api, Resource
from config import DevConfig
import folium as foll


app = Flask(__name__)
api = Api(app, doc="/docs")	

app.config.from_object(DevConfig)


# Api example - TODO : Remove
@api.route('/hello')
class HelloResource(Resource):
    def get(self):
        return {"message":"Hello World"}

@app.route('/home')
def home():
    return "Hello world from home"

@app.route('/')
def index():
    return 
    

if __name__ == "__main__":
	app.run()
