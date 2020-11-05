"""HTTP server"""
from flask import Flask, render_template, request
import my_functions as mf

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False # To work with utf-8
app.config['JSON_SORT_KEYS'] = False # To save the right order in the dictionaries


@app.route("/", methods=['GET'])
@app.route("/home", methods=['GET'])
def index():
    """Shows the main page"""
    return render_template("main_screen.html")


@app.route("/city-info", methods=['GET'])
def city_info():
    """Processes 'city-info' method"""
    geonameid = request.args.get('geonameid')
    return mf.city_info(geonameid)


@app.route("/page-with-cities", methods=['GET'])
def page_with_cities():
    """Processes 'page-with-cities' method"""
    page = request.args.get('page')
    number = request.args.get('number')
    return mf.page_with_cities(page, number)


@app.route("/two-cities", methods=['GET'])
def two_cities():
    """Processes 'two-cities' method"""
    city1 = request.args.get('city1')
    city2 = request.args.get('city2')
    return mf.two_cities(city1, city2)


@app.route("/name-hint", methods=['GET'])
def name_hint():
    """Processes 'name-hint' method"""
    name = request.args.get('name')
    return mf.name_hint(name)


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8000, debug=True)
