from fastapi import FastAPI, Request

app = FastAPI()

@app.post("/walrus")
async def walrus(request: Request):
    data = await request.json()
    print("📩 Webhook 수신됨:", data)

    # walusdt long
    if data.get("id") == "Long":
        print("➡️ 롱 포지션 진입 요청!")
        # place_order(side="Buy")
    # walusdt short
    elif data.get("id") == "Short":
        print("⬅️ 숏 포지션 진입 요청!")
        # place_order(side="Sell")

    return {"status": "ok"}
