from fastapi import FastAPI, Request, BackgroundTasks, HTTPException
from pydantic import BaseModel, HttpUrl
from typing import List, Optional
import time
import httpx
import uuid

app = FastAPI(
    title="Week 11 - API Design Patterns Demo",
    description="Demo CRUD, HATEOAS, Query, and Webhooks patterns using FastAPI"
)

# --- MODELS & DATABASE MOCK ---
class Order(BaseModel):
    id: str
    item: str
    status: str
    amount: float
    links: Optional[List[dict]] = None

orders_db = {
    "ord_001": {"id": "ord_001", "item": "Laptop", "status": "pending", "amount": 1200.0},
    "ord_002": {"id": "ord_002", "item": "Mouse", "status": "shipped", "amount": 25.0},
}

# Webhook subscribers
webhooks_db = []

class WebhookSubscription(BaseModel):
    target_url: HttpUrl

# --- HELPERS ---
def add_hateoas_links(order_id: str):
    return [
        {"rel": "self", "href": f"/orders/{order_id}", "method": "GET"},
        {"rel": "cancel", "href": f"/orders/{order_id}/cancel", "method": "POST"},
        {"rel": "pay", "href": f"/orders/{order_id}/pay", "method": "POST"},
    ]

async def trigger_webhooks(event_type: str, data: dict):
    """Event-driven: Simulation of sending webhooks to subscribers"""
    async with httpx.AsyncClient() as client:
        for url in webhooks_db:
            try:
                # Simulating external notification
                print(f"[Webhook] Sending {event_type} to {url}...")
                await client.post(str(url), json={"event": event_type, "data": data})
            except Exception as e:
                print(f"[Webhook] Failed to send to {url}: {e}")

# --- API ENDPOINTS ---

# 1. CRUD & Query Pattern
@app.get("/orders", response_model=List[Order], tags=["CRUD & Query"])
async def get_orders(item: Optional[str] = None):
    """Query pattern: Filter orders by item name"""
    results = []
    for o_id, o_data in orders_db.items():
        if item and item.lower() not in o_data["item"].lower():
            continue
        order = Order(**o_data)
        order.links = add_hateoas_links(o_id)  # HATEOAS pattern
        results.append(order)
    return results

@app.post("/orders", status_code=201, tags=["CRUD"])
async def create_order(item: str, amount: float):
    order_id = f"ord_{uuid.uuid4().hex[:6]}"
    new_order = {"id": order_id, "item": item, "status": "pending", "amount": amount}
    orders_db[order_id] = new_order
    return {"message": "Order created", "order_id": order_id}

# 2. HATEOAS Pattern (Embedded in GET /orders/{id})
@app.get("/orders/{order_id}", response_model=Order, tags=["HATEOAS"])
async def get_order(order_id: str):
    if order_id not in orders_db:
        raise HTTPException(status_code=404, detail="Order not found")
    data = orders_db[order_id]
    order = Order(**data)
    order.links = add_hateoas_links(order_id)
    return order

# 3. Event-driven & Webhook Pattern
@app.post("/orders/{order_id}/pay", tags=["Event-driven"])
async def pay_order(order_id: str, background_tasks: BackgroundTasks):
    if order_id not in orders_db:
        raise HTTPException(status_code=404, detail="Order not found")
    
    orders_db[order_id]["status"] = "paid"
    
    # Event-driven: Trigger webhook notification in background
    background_tasks.add_task(trigger_webhooks, "order.paid", orders_db[order_id])
    
    return {"message": "Payment successful", "status": "paid"}

@app.post("/webhooks/subscribe", tags=["Webhooks"])
async def subscribe_webhook(sub: WebhookSubscription):
    """Allow other systems to subscribe to our events"""
    webhooks_db.append(sub.target_url)
    return {"message": "Subscribed successfully", "total_subscribers": len(webhooks_db)}

# 4. Simulation of a Webhook receiver (for demo purpose)
@app.post("/demo-receiver", tags=["Demo Receiver"])
async def demo_receiver(request: Request):
    payload = await request.json()
    print(f"[Receiver] Received payload: {payload}")
    return {"status": "received"}

@app.get("/", tags=["Home"])
def home():
    return {
        "message": "Week 11 - API Design Patterns Demo",
        "patterns": ["CRUD", "Query", "HATEOAS", "Event-driven", "Webhooks"],
        "docs": "/docs"
    }
