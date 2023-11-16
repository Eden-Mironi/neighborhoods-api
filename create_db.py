# SQL databases are well-suited for structured data with well-defined schemas. 
# Furthermore, we need to perform aggregations, such as calculating average age or income for a neighborhood, SQL databases are designed for such operations.

# On the other hand, NoSQL are better use if the data model is expected to evolve frequently, and requires flexibility in the schema.
# NoSQL databases allow for a more dynamic schema, accommodating changes without requiring a predefined structure.

# In this case, given the structured nature of your data model, the need for complex queries, and the presence of relationships, a SQL database seems well-suited for this use case. 

import json
from app import db, City, Neighborhood, Resident

# Create the database
db.create_all()

# Load data from neighborhoods_data.json
with open('neighborhoods_data.json', 'r', encoding='utf-8') as file:
    neighborhoods_data = json.load(file)

# Add cities to the database
cities_data = list({neighborhood['city'] for neighborhood in neighborhoods_data})
cities = [City(name=city_data) for city_data in cities_data]
db.session.bulk_save_objects(cities)
db.session.commit()

# Map city names to their corresponding IDs
city_name_to_id = {city.name: city.id for city in City.query.all()}

# Add neighborhoods and residents to the database
for neighborhood_data in neighborhoods_data:
    city_id = city_name_to_id[neighborhood_data['city']]

    
    curr_neighborhood = Neighborhood(name = neighborhood_data['neigborhood'],city_id=city_id, average_age=neighborhood_data['average age'], distance_from_city_center= neighborhood_data['distance from city center'], average_income=neighborhood_data['average income'], public_transport_availability=neighborhood_data['public transport availability'], latitude=neighborhood_data['latitude'], longitude=neighborhood_data['longitude'])
    db.session.add(curr_neighborhood)
    
    residents_data = neighborhood_data.pop('residents', [])

    residents = [Resident(neighborhood_id=curr_neighborhood.id, **resident_data) for resident_data in residents_data]
    db.session.bulk_save_objects(residents)

# Commit the changes
db.session.commit()
