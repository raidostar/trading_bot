from fastapi import FastAPI, Request

app = FastAPI()

@app.post("/")
async def webhook(request: Request):
    data = await request.json()
    print("📩 Webhook 수신됨:", data)

    # 예: Long 진입이면 주문 실행
    if data.get("id") == "Long":
        print("➡️ 롱 포지션 진입 요청!")
        # place_order(side="Buy")

    elif data.get("id") == "Short":
        print("⬅️ 숏 포지션 진입 요청!")
        # place_order(side="Sell")

    return {"status": "ok"}
