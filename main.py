from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="Simple REST API Simulation")

# In-memory database simulation
items_db = {}
item_id_counter = 1

# Pydantic models for request/response validation
class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    quantity: int = 0

class ItemUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    quantity: Optional[int] = None

@app.get("/")
def read_root():
    return {
        "message": "Welcome to the Simple REST API",
        "endpoints": {
            "GET /items": "Get all items",
            "GET /items/{id}": "Get item by ID",
            "POST /items": "Create new item",
            "PUT /items/{id}": "Update item",
            "DELETE /items/{id}": "Delete item"
        }
    }

@app.get("/items")
def get_all_items():
    """Get all items from the database"""
    return {"items": list(items_db.values()), "count": len(items_db)}

@app.get("/items/{item_id}")
def get_item(item_id: int):
    """Get a specific item by ID"""
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return items_db[item_id]

@app.post("/items", status_code=201)
def create_item(item: Item):
    """Create a new item"""
    global item_id_counter
    
    new_item = {
        "id": item_id_counter,
        **item.dict()
    }
    items_db[item_id_counter] = new_item
    item_id_counter += 1
    
    return {"message": "Item created successfully", "item": new_item}

@app.put("/items/{item_id}")
def update_item(item_id: int, item_update: ItemUpdate):
    """Update an existing item"""
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    
    # Update only provided fields
    stored_item = items_db[item_id]
    update_data = item_update.dict(exclude_unset=True)
    
    for key, value in update_data.items():
        stored_item[key] = value
    
    return {"message": "Item updated successfully", "item": stored_item}

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    """Delete an item"""
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    
    deleted_item = items_db.pop(item_id)
    return {"message": "Item deleted successfully", "item": deleted_item}


