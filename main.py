import os
import uuid
from typing import List, Dict
from fastapi import FastAPI, HTTPException, status, Response
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

# --- Ensure the 'static' directory exists ---
if not os.path.exists("static"):
    os.makedirs("static")  # Creates the 'static' folder if it doesn't exist

# --- Pydantic Models ---

# Model for creating an item (input data)
class ItemCreate(BaseModel):
    text: str = Field(..., min_length=1, description="The text content of the item (must not be empty)")
    is_done: bool = False

# Model for representing an item (includes auto-generated UUID)
class ItemResponse(BaseModel):
    id: uuid.UUID
    text: str
    is_done: bool

    # Configuration for Pydantic v2 (similar to orm_mode in v1)
    model_config = {
        "from_attributes": True
    }

# --- In-Memory Storage ---
# Using a dictionary with UUID as the key
items_db: Dict[uuid.UUID, ItemResponse] = {}

# --- FastAPI App ---
app = FastAPI(
    title="Advanced Todo API",
    description="Example FastAPI application with CRUD operations and favicon handling.",
    version="1.0.0",
)

# Mount static files (serving files from the 'static' directory)
app.mount("/static", StaticFiles(directory="static"), name="static")

# --- Utility Endpoints ---

@app.get(
    "/favicon.ico",
    status_code=status.HTTP_204_NO_CONTENT,
    include_in_schema=False  # Hides the route from API docs
)
async def favicon():
    """
    Endpoint to handle browser requests for favicon.ico.
    Returns a No Content status to avoid logging 404 errors.
    """
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.get("/", tags=["General"])
async def root():
    """
    Root endpoint providing a simple greeting.
    """
    return {"Hello": "World", "message": "Greetings from Salford, UK on this fine Tuesday evening!"}

# --- Item API Endpoints ---

@app.post(
    "/items",
    response_model=ItemResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Items"],
    summary="Create a new item",
    description="Creates a new item with the provided text and returns it with a unique UUID."
)
async def create_item(item_in: ItemCreate):
    """
    Creates a new item.
    - **text**: The item text (required).
    - **is_done**: Completion status (default: False).
    """
    item_id = uuid.uuid4()
    new_item = ItemResponse(id=item_id, text=item_in.text, is_done=item_in.is_done)
    items_db[item_id] = new_item
    return new_item

@app.get(
    "/items",
    response_model=List[ItemResponse],
    tags=["Items"],
    summary="List all items",
    description="Retrieves a list of all items with optional pagination."
)
async def list_items(skip: int = 0, limit: int = 10):
    """
    Lists all items with optional pagination.
    - **skip**: Number of items to skip from the start.
    - **limit**: Maximum number of items to return.
    """
    all_items = list(items_db.values())
    return all_items[skip: skip + limit]

@app.get(
    "/items/{item_id}",
    response_model=ItemResponse,
    tags=["Items"],
    summary="Retrieve a specific item",
    description="Retrieves a single item by its unique UUID."
)
async def get_item(item_id: uuid.UUID):
    """
    Retrieves an item by its UUID.
    - **item_id**: The UUID of the item to fetch.
    """
    item = items_db.get(item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with ID {item_id} not found"
        )
    return item

@app.put(
    "/items/{item_id}",
    response_model=ItemResponse,
    tags=["Items"],
    summary="Update an existing item",
    description="Updates an item's text and/or completion status using its UUID."
)
async def update_item(item_id: uuid.UUID, item_update: ItemCreate):
    """
    Updates an existing item.
    - **item_id**: The UUID identifying the item.
    - **item_update**: Object containing updated fields (`text` and `is_done`).
    """
    item = items_db.get(item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with ID {item_id} not found"
        )
    item.text = item_update.text
    item.is_done = item_update.is_done
    items_db[item_id] = item  # Save the updated item
    return item

@app.delete(
    "/items/{item_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Items"],
    summary="Delete an item",
    description="Deletes an item from storage identified by its UUID."
)
async def delete_item(item_id: uuid.UUID):
    """
    Deletes an item by its UUID.
    - **item_id**: The UUID of the item to delete.
    """
    if item_id not in items_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with ID {item_id} not found"
        )
    del items_db[item_id]
    return None

# --- How to Run ---
# 1. Save this script as main.py (or your preferred filename).
# 2. Install dependencies: pip install fastapi "uvicorn[standard]" pydantic
# 3. Run the application using the command:
#       uvicorn main:app --reload
# 4. Open your browser and go to:
#       http://127.0.0.1:8000/docs
#    to see the interactive API documentation.
