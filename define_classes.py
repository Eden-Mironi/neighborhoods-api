def define_classes(db):
    class City(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(50), nullable=False, index=True)

        neighborhoods = db.relationship('Neighborhood', backref='city', lazy=True)

    class Neighborhood(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(50), nullable=False, index=True)
        average_age = db.Column(db.Integer, index=True)
        distance_from_city_center = db.Column(db.Float, index=True)
        average_income = db.Column(db.Integer, index=True)
        public_transport_availability = db.Column(db.String(20))
        latitude = db.Column(db.Float)
        longitude = db.Column(db.Float)

        city_id = db.Column(db.Integer, db.ForeignKey('city.id'), nullable=False, index=True)

        residents = db.relationship('Resident', backref='neighborhood', lazy=True)

        def serialize(self):
            return {
                'id': self.id,
                'neighborhood': self.name,
                'average age': self.average_age,
                'distance from city center': self.distance_from_city_center,
                'average income': self.average_income,
                'public transport availability': self.public_transport_availability,
                'latitude': self.latitude,
                'longitude': self.longitude,
                'city id': self.city_id,
                'residents': self.residents
            }

    class Resident(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        age = db.Column(db.Integer)
        income = db.Column(db.Integer)

        neighborhood_id = db.Column(db.Integer, db.ForeignKey('neighborhood.id'), nullable=False)

    return City, Neighborhood, Resident
