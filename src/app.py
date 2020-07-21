"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Apellido")


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET', 'POST'])
@app.route('/members/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def handle_hello(id =None):

    members = jackson_family.get_all_members()
    response_body = {
        "family": members
    }


    if request.method == "GET":
        if id is not None:
            for member in response_body["family"]:
                if (id == member["id"]):
                    return jsonify(member), 200
        else:
            return jsonify(response_body), 200
    if request.method == "POST":

        return jsonify({"msg": "ingresando por el metodo POST"}), 200
    if request.method == "PUT":
        return jsonify({"msg": "ingresando por el metodo PUT"}), 200
    if request.method == "DELETE":
        return jsonify({"msg": "ingresando por el metodo DELETE"}), 200
    # this is how you can use the Family datastructure by calling its methods
    


    return jsonify(response_body), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
