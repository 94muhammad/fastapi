# Advanced Todo API

A modern, RESTful Todo API built with FastAPI that provides a complete set of CRUD operations for managing todo items. This API demonstrates best practices in FastAPI development, including proper error handling, data validation, and API documentation.

## Features

- 🔄 Complete CRUD operations for todo items
- 🎯 UUID-based item identification
- 📝 Input validation using Pydantic models
- 📚 Automatic API documentation with Swagger UI
- 🚀 Fast and efficient in-memory storage
- 🛡️ Proper error handling and status codes
- 📊 Pagination support for listing items

## Prerequisites

- Python 3.8+
- pip (Python package installer)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd <repository-name>
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install fastapi "uvicorn[standard]" pydantic
```

## Running the Application

Start the server with:
```bash
uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`

## API Documentation

Once the server is running, you can access:
- Swagger UI documentation: `http://127.0.0.1:8000/docs`
- ReDoc documentation: `http://127.0.0.1:8000/redoc`

## API Endpoints

### Create a Todo Item
```bash
curl -X POST "http://127.0.0.1:8000/items" \
     -H "Content-Type: application/json" \
     -d '{"text": "Buy groceries", "is_done": false}'
```

### List All Items
```bash
curl "http://127.0.0.1:8000/items"
```

With pagination:
```bash
curl "http://127.0.0.1:8000/items?skip=0&limit=10"
```

### Get a Specific Item
```bash
curl "http://127.0.0.1:8000/items/{item_id}"
```
Replace `{item_id}` with the actual UUID returned when creating an item.

### Update an Item
```bash
curl -X PUT "http://127.0.0.1:8000/items/{item_id}" \
     -H "Content-Type: application/json" \
     -d '{"text": "Buy groceries", "is_done": true}'
```

### Delete an Item
```bash
curl -X DELETE "http://127.0.0.1:8000/items/{item_id}"
```

## Testing the API

### Using cURL

1. Create a new item:
```bash
curl -X POST "http://127.0.0.1:8000/items" \
     -H "Content-Type: application/json" \
     -d '{"text": "Learn FastAPI", "is_done": false}'
```

2. Copy the returned UUID and use it in subsequent requests:
```bash
# Get the item
curl "http://127.0.0.1:8000/items/{uuid}"

# Update the item
curl -X PUT "http://127.0.0.1:8000/items/{uuid}" \
     -H "Content-Type: application/json" \
     -d '{"text": "Learn FastAPI", "is_done": true}'

# Delete the item
curl -X DELETE "http://127.0.0.1:8000/items/{uuid}"
```

### Using the Swagger UI

1. Open `http://127.0.0.1:8000/docs` in your browser
2. Click on any endpoint to expand it
3. Click "Try it out"
4. Fill in the required parameters
5. Click "Execute" to test the endpoint

## Error Handling

The API includes proper error handling for common scenarios:
- 404 Not Found: When requesting a non-existent item
- 422 Unprocessable Entity: When providing invalid input data
- 204 No Content: For successful deletions

## Contributing

Feel free to submit issues and enhancement requests!