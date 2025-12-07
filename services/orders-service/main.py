
from fastapi import FastAPI
import httpx, os, time

app = FastAPI()
DAPR_PORT = os.getenv("DAPR_HTTP_PORT", "3500")
DAPR_BASE = f"http://localhost:{DAPR_PORT}"

STATE_NAME = "statestore"
PUBSUB_NAME = "messagebus"
TOPIC = "orders.created"

@app.post("/orders")
async def create_order(order: dict):
    enriched = {"id": order["id"], "items": order.get("items", []), "ts": int(time.time()*1000)}
    async with httpx.AsyncClient() as client:
        # 👇 Corrección: usar comillas simples dentro del f-string
        await client.post(
            f"{DAPR_BASE}/v1.0/state/{STATE_NAME}",
            json=[{"key": f"order-{enriched['id']}", "value": enriched}],
            timeout=10
        )
        await client.post(
            f"{DAPR_BASE}/v1.0/publish/{PUBSUB_NAME}/{TOPIC}",
            json=enriched,
            timeout=10
        )
    return {"ok": True, "id": enriched["id"]}
