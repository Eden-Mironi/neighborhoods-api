from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from define_classes import define_classes
from validation_func import *
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import DataError
from werkzeug.exceptions import BadRequest
from flasgger import Swagger, swag_from


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///neighborhoods.db'  # SQLite database
app.config['SWAGGER'] = {
    'title': 'Neighborhoods',
    'version': '1.0',
}

swagger = Swagger(app)
db = SQLAlchemy(app)

City, Neighborhood, Resident = define_classes(db)

@app.errorhandler(400)
def bad_request(error):
    app.logger.error(error)
    return jsonify({'error': 'Bad Request'}), 400

@app.errorhandler(404)
def not_found(error):
    app.logger.error(error)
    return jsonify({'error': 'Not Found'}), 404

@app.errorhandler(Exception)
def generic_error(error):
    app.logger.error(error)
    return jsonify({'error': 'Internal Server Error'}), 500

# Endpoint for fetching neighborhoods
@app.route('/neighborhoods', methods=['GET'])
@swag_from('swagger/neighborhoods.yml')
def neighborhoods():
    try:
        
        # Get query parameters
        age_range = request.args.get('ageRange')
        max_distance = request.args.get('maxDistance')
        sort_by = request.args.get('sortBy')
        
        # Validate parameters
        validate_params(request.args.keys())
        validate_age_range(age_range)
        validate_max_distance(max_distance)
        validate_sort_by(sort_by)

        # Construct the base query
        query = db.session.query(Neighborhood)

        # Apply filters based on request parameters
        if age_range:
            min_age, max_age = map(int, age_range.split(','))
            query = query.filter(Neighborhood.average_age.between(min_age, max_age))

        if max_distance is not None:
            query = query.filter(Neighborhood.distance_from_city_center < max_distance)

        # Apply sorting based on request parameter
        if sort_by:
            field, order = map(str, sort_by.split(','))
            validate_sort_field(field)
            validate_sort_order(order)
            if order.lower() == 'asc':
                query = query.order_by(getattr(Neighborhood, field).asc())
            elif order.lower() == 'desc':
                query = query.order_by(getattr(Neighborhood, field).desc())

        # Execute the query and convert the results to JSON
        neighborhoods  = []
        for neighborhood in query.all():
            curr = neighborhood.serialize()
            curr.pop("id")
            curr.pop("residents")
            city_id = curr.pop("city id")
            city = City.query.filter_by(id=city_id).first()
            if not city:
                raise NoResultFound('City not found')
            curr["city"] = city.name
            neighborhoods.append(curr)
        
        # Return the result in JSON format
        return jsonify(neighborhoods)
    
    except BadRequest as e:
        app.logger.error(e)
        return jsonify({'error': f'Bad Request: {str(e.description)}'}), 400

    except (ValueError, NoResultFound, DataError) as e:
        app.logger.error(e)
        return jsonify({'error': str(e)}), 400

    except Exception as e:
        app.logger.error(e)
        return jsonify({'error': 'Internal Server Error'}), 500
    
if __name__ == '__main__':
    app.run(debug=True)

