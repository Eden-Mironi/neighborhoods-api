
# Validation functions
def validate_params(params):
    if any(item not in ["ageRange", "maxDistance", "sortBy"] for item in params):
        raise ValueError('Invalid parameter')
    
def validate_age_range(age_range):
    if age_range:
        try:
            min_age, max_age = map(int, age_range.split(','))
            if not (0 <= min_age <= max_age):
                raise ValueError('Invalid age range')
        except (ValueError, TypeError):
            raise ValueError('Invalid age range format')

def validate_max_distance(max_distance):
    if max_distance is not None:
        try:
            max_distance = float(max_distance)
            if max_distance < 0:
                raise ValueError('Max distance must be a non-negative number')
        except (ValueError, TypeError):
            raise ValueError('Invalid max distance format')

def validate_sort_by(sort_by):
    if sort_by:
        if ',' not in sort_by:
            raise ValueError('Invalid sort_by format')

def validate_sort_field(field):
    valid_sort_fields = ['name', 'average_age', 'distance_from_city_center', 'average_income', 'public_transport_availability', 'city_id', 'latitude', 'longitude']

    if field not in valid_sort_fields:
        raise ValueError('Invalid sort field')

def validate_sort_order(order):
    if order.lower() not in ('asc', 'desc'):
        raise ValueError('Invalid sort order')