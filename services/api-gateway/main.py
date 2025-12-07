from fastapi import FastAPI
import httpx, os

app = FastAPI()
DAPR_PORT = os.getenv("DAPR_HTTP_PORT", "3500")
DAPR_BASE = f"http://localhost:{DAPR_PORT}"

@app.post("/api/orders")
async def create_order(order: dict):
    url = f"{DAPR_BASE}/v1.0/invoke/orders-service/method/orders"
    async with httpx.AsyncClient() as client:
        r = await client.post(url, json=order, timeout=10)
    return {"status_code": r.status_code, "data": r.json()}
