# Neighborhoods API

The Neighborhoods API is designed to provide information about different neighborhoods, allowing users to query and filter data based on various metrics.

## Table of Contents

- [Overview](#overview)
- [API Endpoints](#api-endpoints)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
  - [Fetching Neighborhoods](#fetching-neighborhoods)
  - [Query Parameters](#query-parameters)
- [Examples](#examples)
- [Error Handling](#error-handling)
- [Testing](#testing)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [License](#license)

## Overview

The Neighborhoods API allows users to retrieve information about different neighborhoods, filter results based on age, distance from the city center, and average income, and sort the data according to various criteria.

## API Endpoints

- **GET `/neighborhoods`**: Fetch a list of neighborhoods with optional filters and sorting.

## Getting Started

### Prerequisites

- [Python]
- [Flask]
- [Flask-SQLAlchemy]
- [flasgger]

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/eden-mironi/neighborhoods-api.git
   ```

2. Navigate to the project directory:

   ```bash
   cd neighborhoods-api
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Fetching Neighborhoods

To retrieve a list of neighborhoods, make a GET request to the `/neighborhoods` endpoint.

### Query Parameters

The `/neighborhoods` endpoint supports the following query parameters:

- **`ageRange`**: Filter neighborhoods by age range (e.g., `ageRange=20,40`).
- **`maxDistance`**: Filter neighborhoods by maximum distance from the city center (e.g., `maxDistance=50`).
- **`sortBy`**: Sort neighborhoods by a specific field and order (e.g., `sortBy=average_age,desc`).

## Examples

### Fetch All Neighborhoods

```bash
curl -X GET http://localhost:5000/neighborhoods
```

### Filter by Age Range and Sort by Income

```bash
curl -X GET "http://localhost:5000/neighborhoods?ageRange=30,50&sortBy=average_income,asc"
```

## Error Handling

The API provides detailed error messages for common issues, such as bad requests or internal server errors.

## Testing

To run unit and integration tests, use the following command:

```bash
python test_app.py
```

## Documentation

For detailed API documentation, refer to the [Swagger Documentation](http://localhost:5000/apidocs/index.html) .
Or the YML doc in /swagger/neighborhoods.yml.
