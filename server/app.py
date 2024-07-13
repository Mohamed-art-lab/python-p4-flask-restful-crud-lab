#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Plant  # Import your Plant model

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

# Resource to handle GET and POST requests for all plants
class Plants(Resource):
    def get(self):
        plants = [plant.to_dict() for plant in Plant.query.all()]
        return make_response(jsonify(plants), 200)

    def post(self):
        data = request.get_json()

        new_plant = Plant(
            name=data['name'],
            image=data['image'],
            price=data['price'],
        )

        db.session.add(new_plant)
        db.session.commit()

        return make_response(new_plant.to_dict(), 201)


api.add_resource(Plants, '/plants')

# Resource to handle GET request for a specific plant by ID
class PlantByID(Resource):
    def get(self, id):
        plant = Plant.query.filter_by(id=id).first()
        if not plant:
            return make_response(jsonify({'error': 'Plant not found'}), 404)
        return make_response(jsonify(plant.to_dict()), 200)


api.add_resource(PlantByID, '/plants/<int:id>')

# Resource to handle PATCH request to update a plant
class UpdatePlant(Resource):
    def patch(self, id):
        data = request.get_json()
        plant = Plant.query.filter_by(id=id).first()

        if not plant:
            return make_response(jsonify({'error': 'Plant not found'}), 404)

        if 'is_in_stock' in data:
            plant.is_in_stock = data['is_in_stock']

        db.session.commit()
        return make_response(jsonify(plant.to_dict()), 200)


api.add_resource(UpdatePlant, '/plants/<int:id>')

# Resource to handle DELETE request to delete a plant
class DeletePlant(Resource):
    def delete(self, id):
        plant = Plant.query.filter_by(id=id).first()

        if not plant:
            return make_response(jsonify({'error': 'Plant not found'}), 404)

        db.session.delete(plant)
        db.session.commit()

        return '', 204


api.add_resource(DeletePlant, '/plants/<int:id>')

if __name__ == '__main__':
    app.run(port=5555, debug=True)