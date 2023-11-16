import unittest
from app import app, db, Neighborhood, City
from werkzeug.exceptions import InternalServerError

class TestAPI(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['SQLALCHEMY_ECHO'] = True

        self.app = app.test_client()
        
        # Set up application context
        self.app_context = app.app_context()
        self.app_context.push()
        
        
        db.create_all()

    def tearDown(self):
        # Pop the application context
        self.app_context.pop()
        
        db.session.remove()
        db.drop_all()

    def test_get_neighborhoods_endpoint(self):
        self.app_context = app.app_context()
        self.app_context.push()
        self.tearDown()
        self.setUp()

        # Insert test data into the database
        city = City(name='Test City')
        db.session.add(city)
        neighborhood = Neighborhood(name='Test Neighborhood', average_age=25, distance_from_city_center=30.0, average_income=50000, public_transport_availability='high', latitude=0.0, longitude=0.0, city=city)
        db.session.add(neighborhood)
        db.session.commit()

        # Perform the API request
        response = self.app.get('/neighborhoods?ageRange=20,30&maxDistance=35&sortBy=average_age,asc')
        data = response.get_json()

        # Assert the response
        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(data), 0)
        self.assertEqual(data[0]['neighborhood'], 'Test Neighborhood')

    def test_invalid_request_bad_request(self):
        response = self.app.get('/neighborhoods?invalidParam=foo')
        data = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', data)

    def test_invalid_sort_field_bad_request(self):
        response = self.app.get('/neighborhoods?sortBy=invalidField,asc')
        data = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', data)
        self.assertIn('Invalid sort field', data['error'])

        
    def test_invalid_max_distance_bad_request(self):
        response = self.app.get('/neighborhoods?maxDistance=-1')
        data = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', data)
        self.assertIn('distance', data['error'])

        
    def test_invalid_age_range_bad_request(self):
        response = self.app.get('/neighborhoods?ageRange=21,16')
        data = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', data)
        self.assertIn('Invalid age range', data['error'])

        
    def test_invalid_sort_field_bad_request(self):
        response = self.app.get('/neighborhoods?sortBy=average_age:asc')
        data = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', data)
        self.assertIn('Invalid sort_by format', data['error'])

    def test_invalid_sort_field_bad_request(self):
        response = self.app.get('/neighborhoods?sortBy=average_age,invalidOrder')
        data = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', data)
        self.assertIn('Invalid sort order', data['error'])

    def test_internal_server_error(self):
        with self.assertRaises(InternalServerError) as context:
            raise InternalServerError('Test Internal Server Error')   
            
        response = context.exception.get_response()
        data =  context.exception.get_description()

        self.assertEqual(response.status_code, 500)
        self.assertIn('Error', data)

class TestDatabaseQueries(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_get_neighborhoods_query(self):
        # Insert test data into the database
        city = City(name='Test City')
        db.session.add(city)
        neighborhood = Neighborhood(name='Test Neighborhood', average_age=25, distance_from_city_center=30.0, average_income=50000, public_transport_availability='high', latitude=0.0, longitude=0.0, city=city)
        db.session.add(neighborhood)
        db.session.commit()

        # Perform the query
        result = db.session.query(Neighborhood).filter(Neighborhood.average_age > 20).all()

        self.assertGreater(len(result), 0)

if __name__ == '__main__':
    unittest.main()
