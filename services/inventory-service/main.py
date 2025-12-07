from fastapi import FastAPI, Request

app = FastAPI()

@app.get("/dapr/subscribe")
def subscriptions():
    return [{"pubsubname":"messagebus","topic":"orders.created","route":"/inventory/order-created"}]

@app.post("/inventory/order-created")
async def on_order_created(req: Request):
    order = await req.json()
    print(f"[inventory] recibido {order.get('id')}")
    return {"status":"processed"}
