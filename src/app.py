"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
# from models import Person


app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# Create the jackson family object
jackson_family = FamilyStructure("Jackson")


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


# Generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/members', methods=['GET'])
def get_all_members():
    try:
       return jsonify(jackson_family.get_all_members()), 200
    except Exception as e:
        return jsonify({"error":str(e)}),500
    
@app.route('/members/<int:id>', methods=['GET'])
def get_member(id):
    try:        
        member= jackson_family.get_members(id)
        if member:
         return jsonify(member), 200
        else:
         return jsonify({"error": "Member Not Found"}), 404
    except Exception as e:
        return jsonify({"error":str(e)}),500

@app.route('/members', methods=['POST'])
def add_member():
    try:
        data = request.get_json()
        if not data or "first_name" not in data or "age" not in data or "lucky_numbers" not in data:
            return jsonify({"error": "Missing Member data"}), 400
        jackson_family.add_member(data)
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error":str(e)}),500


@app.route('/members/<int:id>', methods=['DELETE'])
def delete_member(id):
    try:
        success= jackson_family.delete_member(id)
        if success:
            return jsonify({"done":True}), 200
        else:
            return jsonify({"error": "Member Not Found"}), 404
    except Exception as e:
        return jsonify({"error":str(e)}),500

    


# This only runs if `$ python src/app.py` is executed
if __name__ == '__main__':  
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
