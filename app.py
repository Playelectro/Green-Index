from flask import Flask
from config import DevConfig
import folium as foll


app = Flask(__name__)

app.config.from_object(DevConfig)


@app.route('/home')
def home():
    return "Hello world from home"

@app.route('/')
def index():
    return "BLABLALBALBLABLALBAL"
    

if __name__ == "__main__":
	app.run()
