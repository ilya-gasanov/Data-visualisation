from flask import Flask, render_template
from flask_pymongo import PyMongo
from bson import json_util
from utils import group_projects_by_countries, add_lendprojectcost_sum, get_totalcost_fillcolor_allocation,\
    get_alpha3_country_code

app = Flask(__name__)
app.debug = True
app.use_debugger = True
app.use_reloader = True
app.jinja_env.autoescape = False

# read-only user test account
app.config['MONGO_URI'] = "mongodb://test_user:VJBod5g5cmSfNQFz@cluster0-shard-00-00-lxyl6.mongodb.net:27017," \
                          "cluster0-shard-00-01-lxyl6.mongodb.net:27017,cluster0-shard-00-02-lxyl6.mongodb.net:27017/" \
                          "data?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin"
mongo = PyMongo(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/data")
def get_data():
    query = mongo.db.data.find({},
                               {'_id': 0, 'project_name': 1, 'countryname': 1, 'countrycode': 1,
                                'lendprojectcost': 1})

    grouped_by_countries = group_projects_by_countries(query)
    query_with_sums = add_lendprojectcost_sum(grouped_by_countries)
    fillcolor_allocation = get_totalcost_fillcolor_allocation(query_with_sums)
    response_data = {get_alpha3_country_code(country): {
                          "fillColor": fillcolor_allocation[country]['fillColor'],
                          "country_info": list(query_with_sums[country].values())}
                                                    for country in query_with_sums if get_alpha3_country_code(country)}
    return app.response_class(response=json_util.dumps(response_data), status=200, mimetype='application/json')


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8000)
